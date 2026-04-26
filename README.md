# Campus Recruit Analyzer

Campus Recruit Analyzer (CRA) is a project designed to streamline and analyze campus recruitment processes. This repository contains all the necessary documentation, diagrams, and resources to understand and contribute to the project.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Documentation](#documentation)
- [Development Steps](#development-steps)
- [Requirements](#requirements)
- [License](#license)

## Overview
Campus Recruit Analyzer aims to provide a comprehensive solution for managing and analyzing recruitment activities in academic institutions. By leveraging data and structured processes, CRA helps institutions and companies make informed decisions during campus recruitment drives. The project includes detailed documentation, diagrams, and specifications to guide development and usage.

## Screenshots
<img width="1280" height="832" alt="Screenshot 2026-04-17 at 1 48 04 PM" src="https://github.com/user-attachments/assets/e0066b9f-5cd8-482a-92d8-b14e9842b05a" />
<img width="1280" height="832" alt="Screenshot 2026-04-17 at 1 46 01 PM" src="https://github.com/user-attachments/assets/0bd184aa-7ba7-477b-a2cf-7dd3ed21fc98" />


## Features
- Efficient management of recruitment data.
- Analytical tools to evaluate recruitment trends.
- User-friendly interface for recruiters and institutions.
- Comprehensive documentation and diagrams for better understanding.

## Documentation
The repository includes the following documentation to help you understand the project:

- **[Problem Statement](problem_statement.pdf):** A detailed description of the problem the project aims to solve.
- **[Software Requirements Specification (SRS)](software_requirements_specifiactions_(srs).pdf):** A document outlining the functional and non-functional requirements of the system.
- **[ER Diagram and Documentation](er_diagram_and_documentation.pdf):** Entity-Relationship diagram and its explanation.
- **[UML Use Cases](uml_usecases_version_2.0.pdf):** Use case diagrams and scenarios for the system.
- **[LICENSE](LICENSE):** The license under which this project is distributed.

## Development Steps

### Phase 1 — Set up your environment
1. Install Python 3.10+.
2. Create a virtual environment and install dependencies:
   - `PyQt6`
   - `SQLAlchemy`
   - `PyMySQL`
   - `requests` (for LLM API)
   - `cryptography` (for AES-256 email credential storage)
   - `imaplib` (already in stdlib)
3. Install MySQL 8.0 locally and confirm connectivity.
4. Obtain an LLM API key (OpenAI or Gemini) and test a simple API call.

### Phase 2 — Design and create the database schema
1. Define tables for:
   - `users` (student/admin)
   - `companies` (name, role, year, package)
   - `interview_rounds` (round type, difficulty per company)
   - `topics` (name, category, tags)
   - `company_topics` (junction table)
   - `question_bank`
   - `student_progress` (topics marked done by students)
   - `llm_cache` (cached summaries with timestamps)
2. ER Diagram:
<img width="733" height="472" alt="er_diagram" src="https://github.com/user-attachments/assets/147c63b4-e5f8-46ab-9941-134aae98fadf" />



### Phase 3 — Build the authentication and student-facing UI
1. Create a PyQt6 skeleton with:
   - Login window
   - First-launch credential setup screen (for email)
   - Main window with a sidebar
2. Implement Role-Based Access Control (RBAC) for students and admins.

### Phase 4 — Core features: email parsing + LLM roadmap generation
1. Build an IMAP email parser using `imaplib` to scan institutional emails for placement-related information.
2. Extract and store data (company name, role, OA date, deadline) in MySQL.
3. Integrate LLM API to generate preparation roadmaps based on stored data.
4. Cache LLM responses for efficiency.

### Phase 5 — Progress tracking
1. Add a topic-marking UI for each company's preparation screen.
2. Update the `student_progress` table and recalculate completion percentages in real time.
3. Display progress bars on the main dashboard.

### Phase 6 — Testing, documentation, and packaging
1. Write unit tests for core logic (email parser, LLM cache logic, progress calculation).
2. Create user and admin manuals.
3. Provide a `requirements.txt` and setup/install guide.
4. Package the app for easy installation on Windows or Ubuntu.

### UML Class Diagram

### UML Sequence Diagram


## Requirements
To set up and run the Campus Recruit Analyzer, ensure you have the following:
- A compatible development environment.
- Dependencies as specified in the documentation.
- Access to the provided diagrams and specifications for reference.

## License
This project is licensed under the terms specified in the [LICENSE](LICENSE) file.



For any queries or contributions, feel free to raise an issue or submit a pull request.
