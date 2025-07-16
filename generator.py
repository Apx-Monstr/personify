# Generator 
# generates user persona 
import os
import json
import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv
from constants import GEMINI_MODEL, INDENT_SIZE
load_dotenv()
class Generator:
    def __init__(self, inputData: Dict[str, List[Dict]]):
        self.inputData = inputData
        self.persona = ""
        self.rawAnalysis = {}
        self.processedAnalysis = {}
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def createPrompt(self) -> str:
        
        prompt = f"""
                    Based on the following comprehensive user data analysis, generate a detailed user persona in the exact JSON format provided below.

                    RAW INPUT DATA:
                    {json.dumps(self.inputData, indent=INDENT_SIZE)}


                    INSTRUCTIONS:
                    1. Analyze the user's interests, communication style, and behavioral patterns, sentiments from ALL data types
                    2. Infer demographics (age, occupation, location) based on posting patterns, interests, and community engagement
                    3. Determine personality traits using MBTI framework based on communication style and content preferences
                    4. Assess motivations and frustrations from their posts/comments, community interactions and sentiments
                    5. Generate realistic goals and needs based on their digital behavior patterns
                    6. Create a memorable quote that captures their essence and online persona
                    8. Use the raw data context for more accurate and personalized insights

                    OUTPUT FORMAT (JSON):
                    {{
                        "name": "Generated Name (should reflect their online persona)",
                        "age": "25-45 as string (inferred from language style and interests)",
                        "occupation": "Inferred from interests/posts/communities",
                        "status": "Single/Married/Relationship (inferred from content patterns)",
                        "location": "City, Country (inferred from references or community patterns)",
                        "tier_archetype": "Early Adopters/Innovators/Early Majority/Late Majority (based on tech engagement)",
                        "personality": {{
                            "introvert_extravert": "Introvert/Extravert (based on engagement patterns)",
                            "intuition_sensing": "Intuition/Sensing (based on content preferences)", 
                            "feeling_thinking": "Feeling/Thinking (based on decision-making style)",
                            "perceiving_judging": "Perceiving/Judging (based on organization and planning)"
                    }},
                    "motivations": {{
                        "convenience": "1-5 (based on efficiency-seeking behavior)",
                        "speed": "1-5 (based on quick response patterns)",
                        "wellness": "1-5 (based on health/wellness content engagement)",
                        "preferences": "1-5 (based on customization and personalization)",
                        "dietary_needs": "1-5 (based on food/nutrition related content)"
                    }},
                    "behavior_and_habits": [
                        "3-5 detailed behavioral observations based on digital activity patterns",
                        "Include technology usage patterns and platform preferences",
                        "Social interaction styles and community engagement patterns",
                        "Hobby and interest patterns with frequency analysis",
                        "Content consumption and creation habits"
                    ],
                    "frustrations": [
                        "3-5 specific frustrations inferred from posts/comments tone and content",
                        "Technical or process-related issues they mention or imply",
                        "Social or personal challenges evident in their interactions",
                        "Community or platform-specific pain points"
                    ],
                    "goals_and_needs": [
                        "3-5 primary goals based on their interests, posts, and community engagement",
                        "Personal development needs evident from their content",
                        "Professional aspirations inferred from their digital behavior",
                        "Lifestyle preferences and improvement areas",
                        "Social connection and community building needs"
                    ],
                    "quote": "A memorable quote that captures their personality, communication style, and digital persona mindset"
                    }}

                    IMPORTANT: 
                    - Return ONLY the JSON object, no additional text or explanations
                    - Base ALL inferences on the actual data provided
                    - Ensure the persona is realistic and consistent with the observed patterns
                    - Use the raw data context to make more accurate and specific assessments
                    - If it seems to be the official handle of any organisation, or person, creeate persona accordingly
                    """
        
        return prompt
    
    def generatePersona(self) -> Dict[str, Any]:
        prompt = self.createPrompt()
        
        try:
            response = self.model.generate_content(prompt)
            
            persona_text = ""
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    persona_text += part.text + "\n"
            
            persona_text = persona_text.replace('json', '').replace('```', '').strip()
            
            persona = json.loads(persona_text)
            self.persona = persona
            
            return persona
            
        except Exception as e:
            raise Exception(f"Error generating persona: {str(e)}")
    
    def getPersona(self) -> Dict[str, Any]:
        return self.persona if isinstance(self.persona, dict) else {}
    
