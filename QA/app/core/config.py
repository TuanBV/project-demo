"""Application configuration via Pydantic Settings.

All environment-driven values must be read here, not via scattered os.getenv() calls.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Interview Review System"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "sqlite:///./data/app.db"

    max_docx_upload_size_mb: int = 10
    max_text_import_size_kb: int = 2048
    max_answer_length: int = 10000

    evaluator_mode: str = "keyword"

    correct_score_threshold: float = 85
    mostly_correct_score_threshold: float = 65
    partially_correct_score_threshold: float = 40

    fuzzy_full_score_threshold: float = 90
    fuzzy_partial_high_threshold: float = 80
    fuzzy_partial_low_threshold: float = 70

    enable_answer_quality_factor: bool = True
    keyword_only_maximum_score: float = 85

    semantic_provider: str = "disabled"
    log_level: str = "INFO"
    log_answers: bool = True

    default_question_format: str = "MULTIPLE_CHOICE"
    multiple_choice_option_count: int = 4
    multiple_choice_correct_option_count: int = 1
    shuffle_question_options: bool = True
    allow_option_reselection_before_submit: bool = True
    allow_answer_change_after_submit: bool = False
    practice_reveal_answer_immediately: bool = True
    exam_reveal_answer_immediately: bool = False
    auto_generated_questions_active: bool = False
    distractor_generator_mode: str = "rule_based"

    @property
    def max_docx_upload_size_bytes(self) -> int:
        return self.max_docx_upload_size_mb * 1024 * 1024

    @property
    def max_text_import_size_bytes(self) -> int:
        return self.max_text_import_size_kb * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
