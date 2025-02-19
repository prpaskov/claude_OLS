class ClaudePredict:
    """
    A client for interacting with the Anthropic Claude API. Handles API authentication, generates prompts from Hackenburg et al. (2024) datasets to collect Claude predictions, and processes batch requests and responses. 
    """
    
    # Survey question 1 (see https://github.com/kobihackenburg/scaling-LLM-persuasion/blob/main/SI_Appendix.pdf)
    SURVEY_QUESTIONS = {
        'medicaid': "The U.S. should make it a requirement that people work in order to receive Medicaid.",
        'veteran healthcare': "The U.S. should increase privatization of veterans' healthcare.",
        'worker_pensions': "The U.S. should transition pension plans for public workers into privately managed accounts.",
        'foreign_aid': "The U.S. should not decrease foreign aid spending.",
        'solitary_confinement': "The U.S. should not ban the use of solitary confinement for juveniles in prison.",
        'assisted_suicide': "The U.S. should allow terminally ill patients to end their lives via assisted suicide.",
        'border_restrictions': "The U.S. should adopt more restrictions at the U.S. border.",
        'felons_voting': "The U.S. should not deny convicted felons the right to vote.",
        'affirmative_action': "The U.S. should not allow the use of affirmative action programs.",
        'electoral_college': "The U.S. should abolish the electoral college.",
    }

    def __init__(self, 
                 api_key: str, 
                 model: str = "claude-3-opus-20240229"
                 ):
        """
        Initialize the Claude API client.

        Args:
            api_key: Anthropic API key. 
            model: Model identifier to use for requests. Default is "claude-3-opus-20240229"
        """
        self.api_key = api_key
        self.model = model
        self.headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": self.api_key
            }

    def send_prompt(self, 
                    prompt: str, 
                    system_prompt: Optional[str] = None
                    ) -> Optional[Dict]:
        """
        Send a single prompt to the Claude API.

        Args:
            prompt: The user prompt to send.
            system_prompt: System prompt for context (optional).
        Returns:
            API response dictionary or None if request fails.
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=self.headers,
                json=payload,
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending prompt: {e}")
            return None

    def batch_process(self, 
                      prompts: List[str], 
                      system_prompt: Optional[str] = None, 
                      delay: float = 1.0
                      ) -> List[Dict]:
        """
        Process multiple prompts with rate limiting.

        Args:
            prompts: List of prompts to process.
            system_prompt: Optional system prompt for all requests.
            delay: Seconds to wait between requests.

        Returns:
            List of API response dictionaries.
        """
        return [
            response for prompt in prompts
            if (response := self.send_prompt(prompt, system_prompt)) and time.sleep(delay)
        ]

    def extract_number(self, 
                       value: Any) -> Optional[int]:
        """
        Extract a numerical response from API output.

        Args:
            value: API response value to parse.

        Returns:
            Extracted integer or None if parsing fails.
        """
        if not value:
            return None
        
        try:
            if isinstance(value, str):
                value = eval(value)
            if isinstance(value, list) and value:
                return int(value[0].get('text', 0))
        except:
            return None
        return None

    def create_prompt(self, 
                      row: pd.Series) -> str:
        """
        Create a formatted prompt from user data.

        Args:
            row: Pandas Series containing user data.

        Returns:
            Formatted prompt string.
        """
        prompt = f"""USER PROFILE:
        - Political knowledge: {row['political_knowledge']}, where 0 is low and 3 is high
        - Ideological affiliation: {row['ideo_affiliation']}
        - Political affiliation: {row['party_affiliation']}"""
        
        #this section will skip if the observation is treatment and has no message
        if pd.notna(row['treatment_message']) and row['treatment_message'].strip():
            prompt.append(f"\nCONSIDER THE FOLLOWING:\n{row['treatment_message']}")
        
        #ask survey question relevant to given topic
        prompt.append(f"\nSTATEMENT:\n{self.SURVEY_QUESTIONS[row['issue']]}")
        prompt.append("\nPlease respond ONLY with a number from 0 to 100, where:"
                     "\n0 = strongly disagree\n100 = strongly agree")
        
        return "\n".join(prompt)
