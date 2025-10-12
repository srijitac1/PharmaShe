-- Database initialization script for PharmaShe
-- This script creates the necessary tables and initial data

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS pharmashe;

-- Use the database
\c pharmashe;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create research_sessions table
CREATE TABLE IF NOT EXISTS research_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    query TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES research_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create agent_results table
CREATE TABLE IF NOT EXISTS agent_results (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES research_sessions(id) ON DELETE CASCADE,
    agent_type VARCHAR(50) NOT NULL,
    query TEXT NOT NULL,
    result_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create reports table
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES research_sessions(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    report_type VARCHAR(20) NOT NULL CHECK (report_type IN ('pdf', 'excel', 'json')),
    file_path VARCHAR(500),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create drugs table
CREATE TABLE IF NOT EXISTS drugs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255),
    brand_names JSONB,
    drug_class VARCHAR(255),
    mechanism_of_action TEXT,
    indications JSONB,
    dosage_forms JSONB,
    manufacturer VARCHAR(255),
    patent_expiry TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create clinical_trials table
CREATE TABLE IF NOT EXISTS clinical_trials (
    id SERIAL PRIMARY KEY,
    nct_id VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    status VARCHAR(100),
    phase VARCHAR(50),
    study_type VARCHAR(100),
    condition VARCHAR(255),
    intervention VARCHAR(255),
    sponsor VARCHAR(255),
    start_date TIMESTAMP WITH TIME ZONE,
    completion_date TIMESTAMP WITH TIME ZONE,
    enrollment INTEGER,
    location VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create patents table
CREATE TABLE IF NOT EXISTS patents (
    id SERIAL PRIMARY KEY,
    patent_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    inventor VARCHAR(255),
    assignee VARCHAR(255),
    filing_date TIMESTAMP WITH TIME ZONE,
    issue_date TIMESTAMP WITH TIME ZONE,
    expiry_date TIMESTAMP WITH TIME ZONE,
    abstract TEXT,
    claims TEXT,
    drug_name VARCHAR(255),
    therapeutic_area VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create market_data table
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    drug_name VARCHAR(255),
    therapeutic_area VARCHAR(255),
    region VARCHAR(100),
    year INTEGER,
    market_size DECIMAL(15,2),
    growth_rate DECIMAL(5,2),
    competitor_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_research_sessions_user_id ON research_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_results_session_id ON agent_results(session_id);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_drugs_name ON drugs(name);
CREATE INDEX IF NOT EXISTS idx_clinical_trials_nct_id ON clinical_trials(nct_id);
CREATE INDEX IF NOT EXISTS idx_patents_patent_number ON patents(patent_number);
CREATE INDEX IF NOT EXISTS idx_market_data_drug_name ON market_data(drug_name);

-- Insert sample data
INSERT INTO users (email, username, hashed_password, full_name, is_active, is_admin) VALUES
('admin@pharmashe.com', 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HSKz8m2', 'Admin User', TRUE, TRUE),
('researcher@pharmashe.com', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HSKz8m2', 'Research User', TRUE, FALSE)
ON CONFLICT (email) DO NOTHING;

-- Insert sample drugs
INSERT INTO drugs (name, generic_name, brand_names, drug_class, mechanism_of_action, indications, dosage_forms, manufacturer, patent_expiry) VALUES
('Trastuzumab', 'Trastuzumab', '["Herceptin"]', 'Monoclonal Antibody', 'HER2 receptor antagonist', '["Breast Cancer", "Gastric Cancer"]', '["Injection", "IV Infusion"]', 'Roche', '2025-06-15'),
('Pembrolizumab', 'Pembrolizumab', '["Keytruda"]', 'Monoclonal Antibody', 'PD-1 inhibitor', '["Melanoma", "Lung Cancer", "Cervical Cancer"]', '["Injection", "IV Infusion"]', 'Merck', '2028-09-30'),
('Olaparib', 'Olaparib', '["Lynparza"]', 'PARP Inhibitor', 'PARP enzyme inhibitor', '["Ovarian Cancer", "Breast Cancer"]', '["Tablet", "Capsule"]', 'AstraZeneca', '2027-12-20')
ON CONFLICT (patent_number) DO NOTHING;

-- Insert sample clinical trials
INSERT INTO clinical_trials (nct_id, title, status, phase, study_type, condition, intervention, sponsor, start_date, completion_date, enrollment, location) VALUES
('NCT12345678', 'Phase III Study of Novel Breast Cancer Treatment', 'Recruiting', 'Phase III', 'Interventional', 'Breast Cancer', 'Drug: Novel Compound', 'PharmaCorp', '2024-01-01', '2026-12-31', 500, 'United States'),
('NCT87654321', 'Immunotherapy in Ovarian Cancer', 'Active, not recruiting', 'Phase II', 'Interventional', 'Ovarian Cancer', 'Drug: Immunotherapy', 'BioTech Inc', '2023-06-01', '2025-05-31', 200, 'Europe'),
('NCT11223344', 'Combination Therapy for Cervical Cancer', 'Completed', 'Phase I', 'Interventional', 'Cervical Cancer', 'Drug: Combination', 'MedPharma', '2022-01-01', '2023-12-31', 50, 'Asia')
ON CONFLICT (nct_id) DO NOTHING;

-- Insert sample patents
INSERT INTO patents (patent_number, title, inventor, assignee, filing_date, issue_date, expiry_date, abstract, drug_name, therapeutic_area) VALUES
('US12345678', 'Novel Therapeutic Compound for Cancer Treatment', 'Dr. Smith', 'PharmaCorp', '2015-01-15', '2017-06-20', '2035-01-15', 'A novel compound for treating various cancers...', 'Novel Compound', 'Oncology'),
('EP87654321', 'Method of Treating Breast Cancer', 'Dr. Johnson', 'BioTech Inc', '2016-03-10', '2018-09-15', '2036-03-10', 'A method for treating breast cancer using...', 'Breast Cancer Drug', 'Breast Cancer'),
('US11223344', 'Immunotherapy Composition', 'Dr. Brown', 'MedPharma', '2017-05-20', '2019-11-30', '2037-05-20', 'An immunotherapy composition for cancer treatment...', 'Immunotherapy Drug', 'Oncology')
ON CONFLICT (patent_number) DO NOTHING;

-- Insert sample market data
INSERT INTO market_data (drug_name, therapeutic_area, region, year, market_size, growth_rate, competitor_data) VALUES
('Trastuzumab', 'Breast Cancer', 'North America', 2023, 2500.00, 8.5, '{"competitors": ["Pertuzumab", "T-DM1"], "market_share": 35.2}'),
('Pembrolizumab', 'Cervical Cancer', 'Europe', 2023, 1200.00, 15.3, '{"competitors": ["Nivolumab", "Atezolizumab"], "market_share": 28.7}'),
('Olaparib', 'Ovarian Cancer', 'Asia', 2023, 800.00, 22.1, '{"competitors": ["Rucaparib", "Niraparib"], "market_share": 18.9}')
ON CONFLICT DO NOTHING;

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_research_sessions_updated_at BEFORE UPDATE ON research_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_drugs_updated_at BEFORE UPDATE ON drugs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clinical_trials_updated_at BEFORE UPDATE ON clinical_trials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patents_updated_at BEFORE UPDATE ON patents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_market_data_updated_at BEFORE UPDATE ON market_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
