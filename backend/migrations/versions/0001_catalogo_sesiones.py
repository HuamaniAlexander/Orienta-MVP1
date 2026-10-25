from alembic import op

revision="0001"
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    op.execute('CREATE TABLE orienta.app_user (\n\tid VARCHAR(36) NOT NULL, \n\temail VARCHAR(254) NOT NULL, \n\tpassword_hash TEXT NOT NULL, \n\tcreated TIMESTAMP WITH TIME ZONE NOT NULL, \n\tPRIMARY KEY (id), \n\tUNIQUE (email)\n);')
    op.execute('CREATE TABLE orienta.career (\n\tcode SERIAL NOT NULL, \n\tslug VARCHAR(100) NOT NULL, \n\tname VARCHAR(200) NOT NULL, \n\tarea VARCHAR(100) NOT NULL, \n\tarea_code INTEGER NOT NULL, \n\tkind VARCHAR(30) NOT NULL, \n\tcontent JSON NOT NULL, \n\tprofile JSON, \n\tprofile_reviewed BOOLEAN NOT NULL, \n\tversion VARCHAR(64) NOT NULL, \n\tactive BOOLEAN NOT NULL, \n\tPRIMARY KEY (code), \n\tUNIQUE (slug)\n);')
    op.execute('CREATE INDEX ix_orienta_career_area ON orienta.career (area);')
    op.execute('CREATE INDEX ix_orienta_career_name ON orienta.career (name);')
    op.execute('CREATE TABLE orienta.import_batch (\n\tdigest VARCHAR(64) NOT NULL, \n\tcreated TIMESTAMP WITH TIME ZONE NOT NULL, \n\tcounts JSON NOT NULL, \n\tPRIMARY KEY (digest)\n);')
    op.execute('CREATE TABLE orienta.institution (\n\tcode SERIAL NOT NULL, \n\tname VARCHAR(200) NOT NULL, \n\tkind VARCHAR(30) NOT NULL, \n\tPRIMARY KEY (code)\n);')
    op.execute('CREATE TABLE orienta.legacy_code (\n\tfield VARCHAR(64) NOT NULL, \n\tcode INTEGER NOT NULL, \n\tvalue TEXT NOT NULL, \n\tPRIMARY KEY (field, code), \n\tUNIQUE (field, value)\n);')
    op.execute('CREATE TABLE orienta.browser_session (\n\ttoken_hash VARCHAR(64) NOT NULL, \n\tuser_id VARCHAR(36), \n\tcsrf_hash VARCHAR(64) NOT NULL, \n\texpires TIMESTAMP WITH TIME ZONE NOT NULL, \n\tPRIMARY KEY (token_hash), \n\tFOREIGN KEY(user_id) REFERENCES orienta.app_user (id) ON DELETE CASCADE\n);')
    op.execute('CREATE INDEX ix_orienta_browser_session_expires ON orienta.browser_session (expires);')
    op.execute('CREATE TABLE orienta.comparison (\n\tid VARCHAR(36) NOT NULL, \n\tuser_id VARCHAR(36) NOT NULL, \n\tkey VARCHAR(36) NOT NULL, \n\tpayload_hash VARCHAR(64) NOT NULL, \n\tpayload JSON NOT NULL, \n\tresult JSON NOT NULL, \n\tsnapshot JSON NOT NULL, \n\tcreated TIMESTAMP WITH TIME ZONE NOT NULL, \n\tPRIMARY KEY (id), \n\tUNIQUE (user_id, key), \n\tFOREIGN KEY(user_id) REFERENCES orienta.app_user (id) ON DELETE CASCADE\n);')
    op.execute('CREATE INDEX ix_orienta_comparison_user_id ON orienta.comparison (user_id);')
    op.execute('CREATE INDEX ix_orienta_comparison_created ON orienta.comparison (created);')
    op.execute('CREATE TABLE orienta.offer (\n\tid VARCHAR(64) NOT NULL, \n\tlegacy_code INTEGER NOT NULL, \n\tcareer_code INTEGER NOT NULL, \n\tinstitution_code INTEGER NOT NULL, \n\tmodality VARCHAR(30) NOT NULL, \n\tmodality_code INTEGER NOT NULL, \n\tdistrict VARCHAR(80), \n\tlocation_legacy VARCHAR(150) NOT NULL, \n\tmonths INTEGER NOT NULL, \n\tcost NUMERIC(12, 2), \n\tcost_min NUMERIC(12, 2), \n\tcost_max NUMERIC(12, 2), \n\tcost_status VARCHAR(30) NOT NULL, \n\tdetail JSON NOT NULL, \n\tactive BOOLEAN NOT NULL, \n\tPRIMARY KEY (id), \n\tCHECK (months > 0), \n\tCHECK (cost >= 0), \n\tCHECK (cost_min >= 0 AND cost_max >= cost_min), \n\tUNIQUE (legacy_code), \n\tFOREIGN KEY(career_code) REFERENCES orienta.career (code), \n\tFOREIGN KEY(institution_code) REFERENCES orienta.institution (code)\n);')
    op.execute('CREATE INDEX ix_orienta_offer_modality ON orienta.offer (modality);')
    op.execute('CREATE INDEX ix_orienta_offer_career_code ON orienta.offer (career_code);')
    op.execute('CREATE INDEX ix_orienta_offer_district ON orienta.offer (district);')
    op.execute('CREATE INDEX ix_orienta_offer_institution_code ON orienta.offer (institution_code);')
    op.execute('CREATE TABLE orienta.feedback (\n\tid VARCHAR(36) NOT NULL, \n\tcomparison_id VARCHAR(36) NOT NULL, \n\tscore INTEGER NOT NULL, \n\tcomment VARCHAR(500) NOT NULL, \n\tresearch_consent BOOLEAN NOT NULL, \n\tPRIMARY KEY (id), \n\tCHECK (score BETWEEN 1 AND 5), \n\tFOREIGN KEY(comparison_id) REFERENCES orienta.comparison (id) ON DELETE CASCADE\n);')
    op.execute('CREATE INDEX ix_orienta_feedback_comparison_id ON orienta.feedback (comparison_id);')

def downgrade():
    op.execute("DROP TABLE orienta.feedback")
    op.execute("DROP TABLE orienta.offer")
    op.execute("DROP TABLE orienta.comparison")
    op.execute("DROP TABLE orienta.browser_session")
    op.execute("DROP TABLE orienta.legacy_code")
    op.execute("DROP TABLE orienta.institution")
    op.execute("DROP TABLE orienta.import_batch")
    op.execute("DROP TABLE orienta.career")
    op.execute("DROP TABLE orienta.app_user")
