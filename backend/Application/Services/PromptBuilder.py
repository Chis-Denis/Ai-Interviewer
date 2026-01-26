from typing import List, Optional
from Application.Services.llm_data import QuestionData, AnswerData
from Application.Services.PromptLoader import PromptLoader
from Core.config import settings


class PromptBuilder:
    
    def __init__(self, prompt_loader: Optional[PromptLoader] = None):
        prompts_path = settings.PROMPT_TEMPLATES_PATH if settings.PROMPT_TEMPLATES_PATH else None
        self.prompt_loader = prompt_loader or PromptLoader(prompts_path=prompts_path, version=settings.PROMPT_VERSION)
    
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
    
    def build_question_prompt(self, context: str) -> str:
        return self.prompt_loader.render_template("question_prompt", context=context)
    
    def build_summary_prompt(
        self,
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
        
        return self.prompt_loader.render_template("summary_prompt", topic=topic, qa_text=qa_text)
