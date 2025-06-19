from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKeyConstraint, Index, Integer, JSON, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Notifications(Base):
    __tablename__ = 'notifications'

    notification_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    title: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'))
    content: Mapped[str] = mapped_column(String(500, 'utf8mb4_unicode_ci'))
    is_read: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class ScoringRules(Base):
    __tablename__ = 'scoring_rules'

    scoring_rule_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    scoring_key_name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    scoring_type: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'))
    is_objective: Mapped[int] = mapped_column(TINYINT(1))
    scoring_stages: Mapped[Optional[dict]] = mapped_column(JSON)
    scoring_logic_json: Mapped[Optional[dict]] = mapped_column(JSON)
    norm_group_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    description: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Tests(Base):
    __tablename__ = 'tests'

    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    test_type: Mapped[str] = mapped_column(ENUM('aptitude', 'personality'))
    version: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'))
    duration_minutes: Mapped[int] = mapped_column(Integer)
    version_note: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    question_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    is_published: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    questions: Mapped[List['Questions']] = relationship('Questions', back_populates='test')
    report_rules: Mapped[List['ReportRules']] = relationship('ReportRules', back_populates='test')
    report_sten_distribution: Mapped[List['ReportStenDistribution']] = relationship('ReportStenDistribution', back_populates='test')
    reports: Mapped[List['Reports']] = relationship('Reports', back_populates='test')
    test_analytics_by_group: Mapped[List['TestAnalyticsByGroup']] = relationship('TestAnalyticsByGroup', back_populates='test')
    responses: Mapped[List['Responses']] = relationship('Responses', back_populates='test')
    test_question_links: Mapped[List['TestQuestionLinks']] = relationship('TestQuestionLinks', back_populates='test')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('user_id', 'user_id', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    password: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    role: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'))
    user_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(50, 'utf8mb4_unicode_ci'))
    phone: Mapped[Optional[str]] = mapped_column(String(20, 'utf8mb4_unicode_ci'))
    gender: Mapped[Optional[str]] = mapped_column(String(10, 'utf8mb4_unicode_ci'))
    birth_year: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    institution_admins: Mapped[List['InstitutionAdmins']] = relationship('InstitutionAdmins', back_populates='user')
    notices: Mapped[List['Notices']] = relationship('Notices', back_populates='creator')
    qna: Mapped[List['Qna']] = relationship('Qna', foreign_keys='[Qna.answered_by]', back_populates='users')
    qna_: Mapped[List['Qna']] = relationship('Qna', foreign_keys='[Qna.created_by]', back_populates='users_')
    user_deletion_logs: Mapped[List['UserDeletionLogs']] = relationship('UserDeletionLogs', back_populates='user')
    user_profiles: Mapped[List['UserProfiles']] = relationship('UserProfiles', back_populates='user')


class VerificationCodes(Base):
    __tablename__ = 'verification_codes'
    __table_args__ = (
        Index('ix_verification_codes_id', 'id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    type: Mapped[str] = mapped_column(String(10, 'utf8mb4_unicode_ci'))
    code: Mapped[str] = mapped_column(String(5, 'utf8mb4_unicode_ci'))
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class InstitutionAdmins(Base):
    __tablename__ = 'institution_admins'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='fk_institution_admins_user_id'),
        Index('email', 'email', unique=True),
        Index('fk_institution_admins_user_id', 'user_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    institution_type: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'))
    institution_name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    user_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='institution_admins')


class Notices(Base):
    __tablename__ = 'notices'
    __table_args__ = (
        ForeignKeyConstraint(['creator_id'], ['users.user_id'], name='fk_notices_creator_id'),
        Index('fk_notices_creator_id', 'creator_id'),
        Index('ix_notices_id', 'id')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    title: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'))
    content: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    creator_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))

    creator: Mapped[Optional['Users']] = relationship('Users', back_populates='notices')


class Qna(Base):
    __tablename__ = 'qna'
    __table_args__ = (
        ForeignKeyConstraint(['answered_by'], ['users.user_id'], name='fk_qna_answered_by'),
        ForeignKeyConstraint(['created_by'], ['users.user_id'], name='fk_qna_created_by'),
        Index('fk_qna_answered_by', 'answered_by'),
        Index('fk_qna_created_by', 'created_by')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    title: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'))
    content: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    answer: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    is_private: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    created_by: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    answered_by: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))

    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[answered_by], back_populates='qna')
    users_: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[created_by], back_populates='qna_')


class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = (
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='questions_ibfk_1'),
        Index('test_id', 'test_id')
    )

    question_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    question_type: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'))
    status: Mapped[str] = mapped_column(ENUM('waiting', 'approved', 'rejected'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    test_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    usage_type: Mapped[Optional[str]] = mapped_column(ENUM('aptitude', 'personality'))
    question_name: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    question_text: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    instruction: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    question_image_url: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    is_multiple_choice: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    order_index: Mapped[Optional[int]] = mapped_column(Integer)
    review_comment: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    correct_explanation: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    wrong_explanation: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    test: Mapped[Optional['Tests']] = relationship('Tests', back_populates='questions')
    options: Mapped[List['Options']] = relationship('Options', back_populates='question')
    question_stats_by_group: Mapped[List['QuestionStatsByGroup']] = relationship('QuestionStatsByGroup', back_populates='question')
    responses: Mapped[List['Responses']] = relationship('Responses', back_populates='question')
    test_question_links: Mapped[List['TestQuestionLinks']] = relationship('TestQuestionLinks', back_populates='question')


class ReportRules(Base):
    __tablename__ = 'report_rules'
    __table_args__ = (
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='report_rules_ibfk_1'),
        Index('test_id', 'test_id')
    )

    rule_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    sten_descriptions: Mapped[dict] = mapped_column(JSON)

    test: Mapped['Tests'] = relationship('Tests', back_populates='report_rules')


class ReportStenDistribution(Base):
    __tablename__ = 'report_sten_distribution'
    __table_args__ = (
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='report_sten_distribution_ibfk_1'),
        Index('test_id', 'test_id')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    group_type: Mapped[str] = mapped_column(ENUM('overall', 'school', 'region', 'company'))
    group_value: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    month: Mapped[Optional[int]] = mapped_column(Integer)
    sten_1: Mapped[Optional[int]] = mapped_column(Integer)
    sten_2: Mapped[Optional[int]] = mapped_column(Integer)
    sten_3: Mapped[Optional[int]] = mapped_column(Integer)
    sten_4: Mapped[Optional[int]] = mapped_column(Integer)
    sten_5: Mapped[Optional[int]] = mapped_column(Integer)
    sten_6: Mapped[Optional[int]] = mapped_column(Integer)
    sten_7: Mapped[Optional[int]] = mapped_column(Integer)
    sten_8: Mapped[Optional[int]] = mapped_column(Integer)
    sten_9: Mapped[Optional[int]] = mapped_column(Integer)
    sten_10: Mapped[Optional[int]] = mapped_column(Integer)

    test: Mapped['Tests'] = relationship('Tests', back_populates='report_sten_distribution')


class Reports(Base):
    __tablename__ = 'reports'
    __table_args__ = (
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='reports_ibfk_1'),
        Index('test_id', 'test_id')
    )

    report_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    test_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    score_total: Mapped[Optional[float]] = mapped_column(Float)
    score_standardized: Mapped[Optional[float]] = mapped_column(Float)
    score_level: Mapped[Optional[str]] = mapped_column(String(20, 'utf8mb4_unicode_ci'))
    result_summary: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    report_generated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    test: Mapped[Optional['Tests']] = relationship('Tests', back_populates='reports')


class TestAnalyticsByGroup(Base):
    __tablename__ = 'test_analytics_by_group'
    __table_args__ = (
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='test_analytics_by_group_ibfk_1'),
        Index('test_id', 'test_id')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    group_type: Mapped[str] = mapped_column(ENUM('school', 'region', 'company', 'age'))
    group_value: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    month: Mapped[Optional[int]] = mapped_column(Integer)
    avg_total_score: Mapped[Optional[float]] = mapped_column(Float)
    std_total_score: Mapped[Optional[float]] = mapped_column(Float)
    completion_rate: Mapped[Optional[float]] = mapped_column(Float)
    overall_correct_rate: Mapped[Optional[float]] = mapped_column(Float)
    score_distribution_json: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    test: Mapped['Tests'] = relationship('Tests', back_populates='test_analytics_by_group')


class UserDeletionLogs(Base):
    __tablename__ = 'user_deletion_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='fk_user_deletion_logs_user_id'),
        Index('fk_user_deletion_logs_user_id', 'user_id')
    )

    log_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    deleted_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
    user_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    last_company: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    reason: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_deletion_logs')


class UserProfiles(Base):
    __tablename__ = 'user_profiles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.user_id'], name='fk_user_profiles_user_id'),
        Index('fk_user_profiles_user_id', 'user_id')
    )

    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'), primary_key=True)
    school: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    region: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    target_company: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    current_company: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    user_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_profiles')


class Options(Base):
    __tablename__ = 'options'
    __table_args__ = (
        ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='options_ibfk_1'),
        Index('question_id', 'question_id')
    )

    option_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    option_text: Mapped[str] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    option_order: Mapped[int] = mapped_column(Integer)
    is_correct: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    option_image_url: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    question: Mapped['Questions'] = relationship('Questions', back_populates='options')


class QuestionStatsByGroup(Base):
    __tablename__ = 'question_stats_by_group'
    __table_args__ = (
        ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='question_stats_by_group_ibfk_1'),
        Index('question_id', 'question_id')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    group_type: Mapped[str] = mapped_column(ENUM('school', 'region', 'company', 'age'))
    group_value: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    year: Mapped[Optional[int]] = mapped_column(Integer)
    month: Mapped[Optional[int]] = mapped_column(Integer)
    num_responses: Mapped[Optional[int]] = mapped_column(Integer)
    correct_rate: Mapped[Optional[float]] = mapped_column(Float)
    avg_response_time: Mapped[Optional[float]] = mapped_column(Float)
    option_distribution_json: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))

    question: Mapped['Questions'] = relationship('Questions', back_populates='question_stats_by_group')


class Responses(Base):
    __tablename__ = 'responses'
    __table_args__ = (
        ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='responses_ibfk_2'),
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='responses_ibfk_1'),
        Index('question_id', 'question_id'),
        Index('test_id', 'test_id')
    )

    response_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    email: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    test_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    question_id: Mapped[Optional[str]] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    selected_option_ids: Mapped[Optional[dict]] = mapped_column(JSON)
    response_time_sec: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    question: Mapped[Optional['Questions']] = relationship('Questions', back_populates='responses')
    test: Mapped[Optional['Tests']] = relationship('Tests', back_populates='responses')


class TestQuestionLinks(Base):
    __tablename__ = 'test_question_links'
    __table_args__ = (
        ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='test_question_links_ibfk_2'),
        ForeignKeyConstraint(['test_id'], ['tests.test_id'], name='test_question_links_ibfk_1'),
        Index('question_id', 'question_id'),
        Index('test_id', 'test_id')
    )

    id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'), primary_key=True)
    test_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    question_id: Mapped[str] = mapped_column(String(36, 'utf8mb4_unicode_ci'))
    order_index: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    question: Mapped['Questions'] = relationship('Questions', back_populates='test_question_links')
    test: Mapped['Tests'] = relationship('Tests', back_populates='test_question_links')
