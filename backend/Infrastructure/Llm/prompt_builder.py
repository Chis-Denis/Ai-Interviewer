from typing import List, Optional
from Application.Service.llm_data import QuestionData, AnswerData


class PromptBuilder:
    
    @staticmethod
    def build_question_context(
        topic: str,
        existing_questions: Optional[List[QuestionData]],
        previous_answers: Optional[List[AnswerData]],
    ) -> str:
        context_parts = [f"Interview topic: {topic}"]
        
        if existing_questions:
            context_parts.append("\nPreviously asked questions:")
            for q in existing_questions:
                context_parts.append(f"- {q.text}")
        
        if previous_answers:
            context_parts.append("\nPrevious answers:")
            for a in previous_answers:
                context_parts.append(f"- {a.text}")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def build_question_prompt(context: str) -> str:
        return f"""You are an expert interviewer conducting a technical interview.

{context}

Goal:
Ask ONE follow-up question that evaluates real experience, reasoning, and decision-making.

Your task:
- Generate exactly ONE interview question
- The question must be clear, concise, and specific
- The question must NOT repeat previous questions
- The question must build on previous answers if provided
- The question must assess practical understanding, not theory only
- The question must be relevant to the interview topic
- Require explanation of a real situation
- Focus on HOW or WHY
- Be open-ended (not yes/no)
- The questions must be moderately difficult

Quality rules:
- Avoid generic questions
- Avoid textbook theory
- Avoid definitions
- Ask about trade-offs, problems, or decisions
- Yes/no questions

Constraints:
- 2 sentences only
- Maximum 30 words
- No explanation
- No formatting
- No numbering
- No quotes

Important:
If information is missing, ask about that instead of guessing.

Return ONLY the question text."""
    
    @staticmethod
    def build_summary_prompt(
        topic: str,
        questions: List[QuestionData],
        answers: List[AnswerData],
    ) -> str:
        sorted_questions = sorted(questions, key=lambda x: x.question_order)
        answer_map = {a.question_id: a for a in answers}
        
        qa_pairs = []
        for q in sorted_questions:
            answer = answer_map.get(q.question_id)
            if answer:
                qa_pairs.append(f"Q: {q.text}\nA: {answer.text}")
        
        qa_text = "\n\n".join(qa_pairs)
        
        return f"""Analyze the following interview and provide a comprehensive summary.

Interview topic: {topic}

Interview transcript:
{qa_text}

JSON schema (must match exactly):
{{
  "themes": [string, string, string],
  "key_points": [string, string, string, string, string],
  "sentiment_score": number (0.0 to 1.0),
  "sentiment_label": "positive" | "neutral" | "negative",
  "full_summary_text": string
}}

Rules:
- themes: exactly 3 concise themes
- key_points: exactly 5 concise points
- sentiment_score: decimal with max 2 decimals
- sentiment_label must match sentiment_score
- full_summary_text: 2-3 sentences, professional tone
- No new facts, only summarize what was said
- No personal data
- No markdown
- No extra text
- No extra fields

Evaluation rules:
- Be honest and critical
- Use evidence from answers
- Do not assume missing knowledge
- If something was unclear, state it
- If answers lack depth, reflect that

Sentiment meaning:
- positive = clear, confident, experienced answers
- neutral = basic understanding, limited depth
- negative = unclear, shallow, or incorrect answers

If information is missing, explicitly say so. Do not guess.


Return ONLY the JSON."""
