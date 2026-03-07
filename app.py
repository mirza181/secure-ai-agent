import streamlit as st
import time
import re
import random
from rapidfuzz import fuzz, process
from collections import defaultdict
import html

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Secure AI Agent - CS/BCA Academic Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- Session State Initialization --------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your CS/BCA Academic Assistant. Ask me about programming, algorithms, career paths, or any computer science topic."}
    ]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "search_history" not in st.session_state:
    st.session_state.search_history = []

# -------------------- Utility Functions --------------------
def normalize_text(text: str) -> str:
    """Lowercase and remove punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def extract_keywords(text: str) -> list:
    """Return a list of significant words (excluding common stopwords)."""
    stopwords = {"what", "is", "the", "of", "in", "to", "for", "on", "at", "by",
                 "with", "about", "explain", "tell", "me", "define", "describe"}
    words = normalize_text(text).split()
    return [w for w in words if w not in stopwords and len(w) > 2]

def tokenize(text: str) -> set:
    """Return set of words for overlap scoring."""
    return set(normalize_text(text).split())

# -------------------- Knowledge Base Class --------------------
class KnowledgeBase:
    """
    Stores topic entries with keywords and answers.
    Provides search by fuzzy matching against keywords and category fallback.
    """

    def __init__(self):
        self.entries = []
        self.keyword_to_entries = defaultdict(list)
        self.category_answers = {}
        self._build()

    def _build(self):

        # Basic BCA topic
        self.add_entry(
            ["what is bca", "bca course", "bachelor of computer applications"],
            "BCA (Bachelor of Computer Applications) is a 3-year undergraduate degree focused on computer science, programming, databases, networking, and software development.",
            True
        )

        # OOP
        self.add_entry(
            ["oop", "object oriented programming", "oop concepts", "explain oop"],
            "Object Oriented Programming (OOP) is a programming paradigm based on objects and classes. The four main concepts are Encapsulation, Inheritance, Polymorphism, and Abstraction.",
            True
        )

        # Data Structures
        self.add_entry(
            ["data structures", "what is data structure"],
            "Data Structures are ways of organizing and storing data efficiently so that it can be accessed and modified easily. Examples include arrays, linked lists, stacks, queues, trees, and graphs.",
            True
        )

        # Algorithms
        self.add_entry(
            ["algorithm", "what is algorithm"],
            "An algorithm is a step-by-step procedure used to solve a problem or perform a task in computing.",
            True
        )

        # Software Developer Career
        self.add_entry(
            ["software developer", "how to become a software developer", "become developer"],
            "To become a Software Developer: 1) Learn a programming language like Python, Java, or C++. 2) Understand Data Structures and Algorithms. 3) Build projects such as websites or apps. 4) Learn Git and contribute to open source. 5) Practice coding problems (LeetCode, HackerRank). 6) Apply for internships and developer jobs.",
            True
        )

        # AI vs Machine Learning
        self.add_entry(
            ["ai vs machine learning", "difference between ai and ml", "ai and machine learning difference"],
            "Artificial Intelligence (AI) is a broad field that aims to create machines that can perform tasks requiring human intelligence. Machine Learning (ML) is a subset of AI that allows computers to learn from data and improve automatically without being explicitly programmed. In short: AI is the bigger concept, ML is one approach within AI.",
            True
        )
        # OOP Concepts
        self.add_entry(
            ["oop", "oop concepts", "object oriented programming", "explain oop concepts"],
            """Object Oriented Programming (OOP) is a programming paradigm based on objects and classes.

            The four main OOP concepts are:

            1. Encapsulation
            Encapsulation means wrapping data and methods together in a single unit (class) and restricting direct access to some components.

            2. Inheritance
            Inheritance allows a class to inherit properties and methods from another class, promoting code reuse.

            3. Polymorphism
            Polymorphism means the same function or method can behave differently depending on the object.

            4. Abstraction
            Abstraction hides complex implementation details and only shows the essential features of an object.

            These concepts help make programs modular, reusable, and easier to maintain.
            """,
            True
    )


        # Python
        self.add_entry(
            ["python", "python programming"],
            "Python is a high-level programming language known for simplicity, readability, and wide use in web development, AI, data science, and automation.",
            True
        )

    def add_entry(self, keywords: list, answer: str, is_detailed: bool = False):
        """Add a knowledge base entry."""

        entry = {"keywords": [k.lower() for k in keywords], "answer": answer}
        self.entries.append(entry)

        for kw in entry["keywords"]:
            self.keyword_to_entries[kw].append(entry)

        if is_detailed:
            for kw in entry["keywords"]:
                self.category_answers[kw] = answer

    def search(self, query: str, 
    threshold: int = 80) -> str:
        query = query.lower()

        # direct keyword match
        for entry in self.entries:
            for kw in entry["keywords"]:
                if kw in query or query in kw:
                    return entry["answer"]
        """
        Return the best matching answer for the query using fuzzy matching.
        First tries to match against known detailed topics; if none,
        searches all keywords with a scorer and returns the highest scoring answer.
        """
        query_norm = normalize_text(query)
        query_words = set(query_norm.split())

        # 1. Try exact match on detailed topics
        for kw in self.category_answers:
            if kw in query_norm:
                return self.category_answers[kw]

        # 2. Fuzzy match on all keywords
        # collect all unique keywords from entries
        all_keywords = list(self.keyword_to_entries.keys())
        # use rapidfuzz to get best matches
        matches = process.extract(query_norm, all_keywords, scorer=fuzz.token_sort_ratio, limit=10)
        best_score = 0
        best_answer = None
        seen_answers = set()
        for kw, score, _ in matches:
            if score < threshold:
                continue
            for entry in self.keyword_to_entries[kw]:
                if entry["answer"] in seen_answers:
                    continue
                seen_answers.add(entry["answer"])
                # boost score if multiple keywords from query match
                kw_words = set(kw.split())
                overlap = len(query_words & kw_words)
                final_score = score + overlap * 5
                if final_score > best_score:
                    best_score = final_score
                    best_answer = entry["answer"]

        if best_answer:
            return best_answer

        # 3. Fallback: check if query contains any CS/BCA related terms
        cs_terms = ["computer", "science", "bca", "programming", "language", "data",
                    "algorithm", "software", "web", "ai", "ml", "cloud", "cyber",
                    "network", "database", "oop", "java", "python", "c++", "javascript",
                    "html", "css", "sql", "linux", "windows", "macos", "android",
                    "ios", "devops", "docker", "kubernetes", "aws", "azure"]
        if any(term in query_norm for term in cs_terms):
            return "I'm not sure about that specific topic, but it seems related to Computer Science or BCA. Could you rephrase or ask about something else in these fields?"

        return "Sorry, I am designed to answer questions related to Computer Science and BCA only."

# -------------------- Knowledge Base Construction --------------------
kb = KnowledgeBase()

def add_detailed_entry(keywords, answer):
    kb.add_entry(keywords, answer, is_detailed=True)

def add_entry(keywords, answer):
    kb.add_entry(keywords, answer, is_detailed=False)

# ========== BCA – Comprehensive Detailed Answer ==========
add_detailed_entry(
    ["bca", "bachelor of computer applications", "tell me about bca", "explain bca", "bca course"],
    """
### 🎓 BCA (Bachelor of Computer Applications) – Complete Reference

#### 1. Introduction
BCA is a 3‑year undergraduate degree that focuses on computer applications and software development. It equips students with programming skills, database management, networking basics, and software engineering principles. The course is designed to meet the growing demand for IT professionals.

#### 2. Course Duration & Structure
- **Duration**: 3 years (6 semesters)
- **Credit System**: Typically 120–140 credits
- **Examination Pattern**: Semester‑wise exams with internal assessments, projects, and viva

#### 3. Semester‑wise Syllabus (Detailed)

**Semester 1**  
- **Programming in C** – Basics, control structures, arrays, functions, pointers  
- **Mathematics‑I** – Discrete Mathematics (sets, relations, functions, logic)  
- **Digital Electronics** – Number systems, logic gates, combinational circuits  
- **English Communication** – Grammar, writing skills, presentation  

**Semester 2**  
- **Object‑Oriented Programming with C++** – Classes, inheritance, polymorphism, file handling  
- **Data Structures** – Arrays, linked lists, stacks, queues, trees, graphs  
- **Mathematics‑II** – Probability, statistics, linear algebra basics  
- **Financial Accounting** – Fundamentals of accounting, software for accounting  

**Semester 3**  
- **Java Programming** – OOP, collections, multithreading, applets, Swing  
- **Operating Systems** – Processes, scheduling, memory management, file systems  
- **Computer Networks** – OSI model, TCP/IP, IP addressing, routing, network security  
- **Database Management Systems** – ER model, SQL, normalization, transactions  

**Semester 4**  
- **Python Programming** – Syntax, OOP, libraries (NumPy, Pandas), web frameworks  
- **Web Development** – HTML5, CSS3, JavaScript, Bootstrap, PHP/MySQL  
- **Software Engineering** – SDLC, Agile, Scrum, UML, testing  
- **.NET Programming** – C#, ASP.NET, Windows forms  

**Semester 5**  
- **Cloud Computing** – IaaS/PaaS/SaaS, AWS/Azure basics, virtualization  
- **Cyber Security** – Threats, encryption, firewalls, ethical hacking  
- **Electives** – AI, IoT, Data Science, Mobile App Development  
- **Mini Project** – Team‑based project with documentation  

**Semester 6**  
- **Internship** – 2‑3 months industry training  
- **Major Project** – Individual project with report and presentation  
- **Advanced Topics** – Block chain, DevOps, Big Data (optional)

#### 4. Programming Languages Learned
| Language  | Paradigm              | Key Applications                          |
|-----------|-----------------------|-------------------------------------------|
| C         | Procedural            | System programming, embedded              |
| C++       | Object‑oriented       | Games, performance‑critical apps          |
| Java      | OOP, platform‑indep.  | Enterprise, Android                        |
| Python    | Multi‑paradigm        | Web, data science, AI, automation         |
| JavaScript| Event‑driven          | Front‑end, back‑end (Node.js)              |
| SQL       | Declarative           | Database queries                           |
| PHP       | Server‑side scripting | Web development (WordPress, etc.)         |

#### 5. Skills Acquired
- **Technical**: Programming, database design, networking, OS concepts, software engineering
- **Soft Skills**: Problem‑solving, teamwork, communication, project management
- **Tools**: Git, Linux, VS Code, Eclipse, MySQL Workbench, Wireshark

#### 6. Career Opportunities – Expanded
| Job Role                     | Average Salary (India) | Top Recruiters                          |
|------------------------------|------------------------|-----------------------------------------|
| Software Developer           | ₹3.5 – 8 LPA           | TCS, Infosys, Wipro, Accenture          |
| Web Developer                | ₹2.5 – 6 LPA           | Startups, digital agencies              |
| Data Analyst                 | ₹4 – 9 LPA             | Amazon, Flipkart, Deloitte              |
| System Administrator         | ₹3 – 6 LPA             | HCL, Tech Mahindra, IBM                 |
| Network Engineer             | ₹3.5 – 7 LPA           | Cisco, Jio, Airtel                       |
| Cyber security Analyst       | ₹4 – 10 LPA            | KPMG, PwC, EY                            |
| Mobile App Developer         | ₹3.5 – 8 LPA           | Samsung, Xiaomi, startups                |
| Cloud Engineer               | ₹5 – 12 LPA            | AWS, Azure, Google Cloud partners        |
| DevOps Engineer              | ₹6 – 15 LPA            | Amazon, Flipkart, Ola                    |

#### 7. Higher Studies – Detailed
- **MCA (Master of Computer Applications)** – 2 years, specialisations in AI, cloud, etc.
- **MBA in IT** – For management roles in tech companies
- **M.Sc. in Computer Science** – Research‑oriented
- **Data Science / AI certifications** – From IITs, IIITs, Coursera, Udacity
- **Cloud Certifications** – AWS Certified Solutions Architect, Azure Administrator

#### 8. Future Scope & Industry Trends
- **AI & ML Integration**: BCA graduates with AI skills are highly sought after.
- **Cloud & DevOps**: Companies are adopting cloud‑native development.
- **Cyber security**: Growing demand for security analysts.
- **Freelancing**: Platforms like Upwork, Fiverr offer global opportunities.
- **Startups**: Many BCA graduates launch successful tech startups.

#### 9. Salary Trends (India)
- **Entry‑level**: ₹2.5 – 5 LPA
- **Mid‑level (3‑5 years)**: ₹6 – 12 LPA
- **Senior‑level**: ₹15 – 25 LPA (with niche skills)

#### 10. Top Recruiters (India)
TCS, Infosys, Wipro, Accenture, HCL, Tech Mahindra, IBM, Deloitte, Capgemini, Amazon, Microsoft, Oracle, Cisco, and numerous startups.

#### 11. Resources for BCA Students
- **Books**: "Let Us C" by Yashwant Kanetkar, "Java: The Complete Reference" by Herbert Schildt
- **Online Courses**: NPTEL, Coursera, Udemy
- **Practice Platforms**: HackerRank, LeetCode, GeeksforGeeks
- **Communities**: r/BCA, Stack Overflow, GitHub

#### 12. Frequently Asked Questions (FAQs)
**Q1. Can I do BCA without Maths?**  
A1. Most universities require Maths in 10+2. Some accept Statistics or Computer Science as alternatives.

**Q2. Is BCA better than B.Sc. Computer Science?**  
A2. BCA is more application‑oriented, while B.Sc. CS has more theory. Both lead to similar careers.

**Q3. Can I get a job in MNCs after BCA?**  
A3. Yes, many MNCs hire BCA graduates for software development, testing, and support roles.

**Q4. What is the difference between BCA and B.Tech CS?**  
A4. B.Tech is a 4‑year engineering degree with more focus on hardware and mathematics; BCA is a 3‑year professional degree focused on applications.
"""
)

# ========== Computer Science – Comprehensive Detailed Answer ==========
add_detailed_entry(
    ["computer science", "cs", "tell me about computer science", "explain computer science"],
    """
### 💻 Computer Science – The Complete Guide

#### 1. Introduction
Computer Science (CS) is the study of computers and computational systems. Unlike electrical and computer engineering, computer science deals with software and software systems; this includes their theory, design, development, and application. Principal areas of study include artificial intelligence, computer systems and networks, security, database systems, human‑computer interaction, vision and graphics, numerical analysis, programming languages, software engineering, bioinformatics, and theory of computing.

#### 2. Core Areas – In Depth

**2.1 Algorithms and Data Structures**  
- Foundation for efficient problem‑solving  
- Data Structures: arrays, linked lists, stacks, queues, trees, graphs, hash tables  
- Algorithms: sorting (quick, merge, heap), searching (binary, BFS, DFS), dynamic programming, greedy, backtracking  
- Complexity analysis: Big O, Big Ω, Big Θ

**2.2 Computer Architecture**  
- CPU design: ALU, control unit, registers  
- Memory hierarchy: cache, RAM, disk  
- Instruction set architecture (RISC, CISC)  
- Pipelining, superscalar, multi‑core processors

**2.3 Operating Systems**  
- Process management: states, scheduling (FCFS, SJF, Round Robin, Priority)  
- Memory management: paging, segmentation, virtual memory  
- File systems: NTFS, ext4, FAT32  
- Concurrency: threads, synchronization, deadlocks  
- Examples: Windows, Linux, macOS, Android

**2.4 Computer Networks**  
- OSI and TCP/IP models  
- Protocols: HTTP/HTTPS, DNS, SMTP, FTP, TCP, UDP, IP  
- Network devices: routers, switches, hubs, firewalls  
- Network security: encryption, firewalls, VPNs

**2.5 Database Systems**  
- Relational model, SQL, normalization, ACID  
- Indexing, transactions, concurrency control  
- NoSQL databases: document (MongoDB), key‑value (Redis), column (Cassandra), graph (Neo4j)

**2.6 Software Engineering**  
- SDLC: requirements, design, implementation, testing, deployment, maintenance  
- Methodologies: Waterfall, Agile (Scrum, Kanban), DevOps  
- Testing: unit, integration, system, acceptance  
- Version control: Git, GitHub

**2.7 Artificial Intelligence**  
- Machine learning: supervised, unsupervised, reinforcement  
- Deep learning: neural networks (CNN, RNN, GAN)  
- Natural language processing, computer vision, robotics  
- Tools: TensorFlow, PyTorch, scikit‑learn

**2.8 Cyber security**  
- Threats: malware, phishing, DDoS, SQL injection  
- Protection: encryption, firewalls, intrusion detection  
- Ethical hacking, penetration testing  
- Security certifications: CISSP, CEH

**2.9 Theory of Computation**  
- Automata theory: finite automata, pushdown automata, Turing machines  
- Computability: decidability, halting problem  
- Complexity classes: P, NP, NP‑complete

#### 3. Programming Languages in Computer Science
| Language  | Paradigm              | Typical Use Cases                         |
|-----------|-----------------------|-------------------------------------------|
| Python    | Multi‑paradigm        | AI/ML, data science, web, automation     |
| Java      | OOP                   | Enterprise, Android, big data              |
| C/C++     | Procedural/OOP        | System software, games, embedded          |
| JavaScript| Event‑driven          | Web front‑end, back‑end (Node.js)         |
| C#        | OOP                   | Windows apps, game dev (Unity)            |
| Go        | Concurrent            | Cloud services, networking                 |
| Rust      | Systems               | Safe system programming                    |
| SQL       | Declarative           | Database queries                           |

#### 4. Career Opportunities
- **Software Engineer/Developer** – Design and build applications  
- **Data Scientist** – Extract insights from data using ML  
- **AI/ML Engineer** – Develop AI models and systems  
- **Cyber security Analyst** – Protect systems from threats  
- **Cloud Architect** – Design cloud infrastructure  
- **DevOps Engineer** – Automate deployment and operations  
- **Game Developer** – Create games using Unity/Unreal  
- **Mobile App Developer** – iOS/Android apps  
- **IT Consultant** – Advise businesses on technology  

#### 5. Future Scope
- **Quantum Computing** – Solving complex problems exponentially faster  
- **Edge Computing** – Processing data near the source  
- **Blockchain** – Decentralized ledgers for trust  
- **Bioinformatics** – Using CS to understand biological data  
- **Human‑Computer Interaction** – Better interfaces and experiences

#### 6. Resources for CS Students
- **Books**: "Introduction to Algorithms" (CLRS), "Clean Code" (Martin), "The Pragmatic Programmer"  
- **Online Courses**: MIT OpenCourseWare, Coursera, edX  
- **Practice Platforms**: LeetCode, HackerRank, Codeforces, Kaggle  
- **Communities**: Stack Overflow, GitHub, Reddit r/computerscience

#### 7. FAQs
**Q1. What is the difference between Computer Science and Computer Engineering?**  
A1. Computer Science focuses on software, algorithms, and theory; Computer Engineering blends hardware and software (digital logic, microprocessors).

**Q2. Can I learn Computer Science on my own?**  
A2. Yes, many resources are available online. A degree helps with structured learning and placements.

**Q3. Is math required for CS?**  
A3. Yes, discrete math, linear algebra, probability, and calculus are important.

**Q4. Which programming language should I learn first?**  
A4. Python is often recommended for beginners due to its simplicity and wide application.
"""
)

# ========== Artificial Intelligence – Detailed ==========
add_detailed_entry(
    ["artificial intelligence", "ai", "what is ai", "explain ai"],
    """
### 🤖 Artificial Intelligence (AI) – In‑Depth Guide

#### 1. Definition
Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (acquiring information and rules for using it), reasoning (using rules to reach conclusions), and self‑correction.

#### 2. Branches of AI
- **Machine Learning** – Algorithms that improve through experience.
- **Deep Learning** – Neural networks with many layers.
- **Natural Language Processing** – Enabling computers to understand human language.
- **Computer Vision** – Interpreting visual information.
- **Robotics** – Building intelligent robots.
- **Expert Systems** – Mimicking human expertise.

#### 3. Applications
- Virtual assistants (Siri, Alexa)
- Recommendation systems (Netflix, Amazon)
- Autonomous vehicles
- Healthcare diagnostics
- Fraud detection
- Gaming AI

#### 4. Future of AI
AI is expected to revolutionize industries, create new job roles, and raise ethical questions about privacy, bias, and automation. Research areas include explainable AI, general AI, and AI safety.

#### 5. Key Concepts
- **Turing Test** – A test of a machine's ability to exhibit intelligent behaviour.
- **Strong AI vs Weak AI** – Strong AI possesses consciousness; weak AI is task‑specific.
- **Supervised, Unsupervised, Reinforcement Learning** – Core ML paradigms.

#### 6. Tools and Frameworks
- **Python Libraries**: TensorFlow, PyTorch, Keras, scikit‑learn
- **Cloud AI Services**: AWS AI, Google AI, Azure AI

#### 7. Career Paths
- AI Engineer
- Machine Learning Engineer
- Data Scientist
- NLP Engineer
- Computer Vision Engineer

#### 8. Resources
- **Books**: "Artificial Intelligence: A Modern Approach" (Russell & Norvig)
- **Courses**: Andrew Ng's Machine Learning (Coursera), Deep Learning Specialization
- **Practice**: Kaggle, AI competitions
"""
)

# ========== Machine Learning – Detailed ==========
add_detailed_entry(
    ["machine learning", "ml", "what is machine learning", "explain ml"],
    """
### 📈 Machine Learning (ML) – Comprehensive Guide

#### 1. What is Machine Learning?
Machine Learning is a subset of AI that enables systems to automatically learn and improve from experience without being explicitly programmed. It uses algorithms to find patterns in data.

#### 2. Types of Machine Learning
- **Supervised Learning** – Model trained on labeled data (e.g., classification, regression).
- **Unsupervised Learning** – Model finds hidden patterns in unlabeled data (e.g., clustering, association).
- **Reinforcement Learning** – Model learns through trial and error using rewards and punishments.

#### 3. Common Algorithms
- Linear Regression, Logistic Regression
- Decision Trees, Random Forest
- Support Vector Machines (SVM)
- k‑Nearest Neighbors (k‑NN)
- K‑Means Clustering
- Neural Networks

#### 4. Applications
- Spam filtering
- Image recognition
- Stock market prediction
- Customer segmentation
- Recommendation engines

#### 5. Tools & Libraries
- Python: scikit‑learn, TensorFlow, PyTorch, Keras
- R: caret, randomForest
- Big data: Apache Spark MLlib

#### 6. Important Concepts
- **Training/Test Split**
- **Overfitting & Underfitting**
- **Bias‑Variance Tradeoff**
- **Cross‑Validation**
- **Feature Engineering**
- **Model Evaluation Metrics** (accuracy, precision, recall, F1, ROC‑AUC)

#### 7. Career Paths
- Machine Learning Engineer
- Data Scientist
- AI Engineer
- Research Scientist

#### 8. Resources
- **Books**: "Pattern Recognition and Machine Learning" (Bishop), "The Elements of Statistical Learning" (Hastie)
- **Courses**: Andrew Ng's Machine Learning (Coursera), Fast.ai
- **Practice**: Kaggle, UCI ML Repository
"""
)

# ========== Cybersecurity – Detailed ==========
add_detailed_entry(
    ["cybersecurity", "cyber security", "what is cybersecurity"],
    """
### 🔒 Cybersecurity – In‑Depth Guide

#### 1. Definition
Cybersecurity is the practice of protecting systems, networks, and programs from digital attacks. These attacks are usually aimed at accessing, changing, or destroying sensitive information, extorting money, or interrupting normal business processes.

#### 2. Key Domains
- **Network Security** – Protecting network infrastructure.
- **Application Security** – Securing software applications.
- **Information Security** – Protecting data integrity and privacy.
- **Identity Management** – Controlling access to resources.
- **Incident Response** – Handling security breaches.
- **Disaster Recovery** – Restoring systems after failures.

#### 3. Common Threats
- Malware (viruses, worms, ransomware)
- Phishing
- Man‑in‑the‑Middle attacks
- Denial of Service (DoS)
- SQL Injection
- Zero‑day exploits

#### 4. Security Measures
- Firewalls, Intrusion Detection Systems (IDS)
- Encryption (AES, RSA)
- Multi‑factor Authentication (MFA)
- Regular patching and updates
- Security awareness training

#### 5. Career Paths
- Security Analyst
- Penetration Tester
- Security Engineer
- Chief Information Security Officer (CISO)
- Forensic Analyst

#### 6. Certifications
- CompTIA Security+
- Certified Ethical Hacker (CEH)
- CISSP
- CISM

#### 7. Resources
- **Books**: "The Web Application Hacker's Handbook", "Hacking: The Art of Exploitation"
- **Online Platforms**: TryHackMe, Hack The Box, OWASP
"""
)

# ========== Cloud Computing – Detailed ==========
add_detailed_entry(
    ["cloud computing", "what is cloud computing"],
    """
### ☁️ Cloud Computing – Detailed Guide

#### 1. Definition
Cloud computing is the on‑demand delivery of IT resources over the internet with pay‑as‑you‑go pricing. Instead of buying, owning, and maintaining physical data centers, you can access technology services, such as computing power, storage, and databases, from a cloud provider.

#### 2. Service Models
- **IaaS (Infrastructure as a Service)** – Provides virtualized computing resources (e.g., AWS EC2, Google Compute Engine).
- **PaaS (Platform as a Service)** – Provides platform for developing and deploying applications (e.g., AWS Elastic Beanstalk, Google App Engine).
- **SaaS (Software as a Service)** – Provides software applications over the internet (e.g., Salesforce, Microsoft 365).

#### 3. Deployment Models
- **Public Cloud** – Services offered over public internet (AWS, Azure, GCP).
- **Private Cloud** – Dedicated infrastructure for a single organization.
- **Hybrid Cloud** – Combination of public and private clouds.

#### 4. Major Providers
- **Amazon Web Services (AWS)** – Market leader, broad range of services.
- **Microsoft Azure** – Strong integration with Microsoft products.
- **Google Cloud Platform (GCP)** – Expertise in data analytics and AI.

#### 5. Benefits
- Scalability
- Cost efficiency
- High availability
- Disaster recovery
- Global reach

#### 6. Key Concepts
- Virtualization
- Containers (Docker, Kubernetes)
- Serverless computing
- Microservices
- DevOps

#### 7. Career Paths
- Cloud Engineer
- Cloud Architect
- DevOps Engineer
- Site Reliability Engineer (SRE)

#### 8. Certifications
- AWS Certified Solutions Architect
- Microsoft Azure Administrator
- Google Professional Cloud Architect
"""
)

# ========== Software Engineering – Detailed ==========
add_detailed_entry(
    ["software engineering", "what is software engineering"],
    """
### 🛠️ Software Engineering – In‑Depth Guide

#### 1. Definition
Software engineering is the systematic application of engineering approaches to the development of software. It involves designing, building, testing, and maintaining software systems.

#### 2. Software Development Life Cycle (SDLC)
- **Requirement Analysis** – Gathering and analyzing user needs.
- **Design** – Creating architecture and detailed design.
- **Implementation** – Writing code.
- **Testing** – Verifying that software meets requirements.
- **Deployment** – Releasing software to users.
- **Maintenance** – Updating and fixing issues.

#### 3. Development Methodologies
- **Waterfall** – Linear sequential model.
- **Agile** – Iterative development with cross‑functional teams.
- **Scrum** – Agile framework with sprints.
- **Kanban** – Visual workflow management.
- **DevOps** – Integrating development and operations.

#### 4. Key Concepts
- **Object‑Oriented Programming** – Encapsulation, inheritance, polymorphism.
- **Design Patterns** – Reusable solutions to common problems.
- **Version Control** – Git, SVN.
- **Testing** – Unit, integration, system, acceptance.
- **Refactoring** – Improving code without changing behavior.

#### 5. Career Paths
- Software Developer/Engineer
- Quality Assurance Engineer
- Software Architect
- Technical Lead
- Project Manager

#### 6. Tools
- **IDEs**: VS Code, IntelliJ, Eclipse
- **Build Tools**: Maven, Gradle
- **CI/CD**: Jenkins, GitLab CI, GitHub Actions
- **Project Management**: Jira, Trello
"""
)

# ========== Programming Languages – Massively Expanded ==========
# We'll generate entries for many languages programmatically
languages = [
    ("python", "Python is a high‑level, interpreted language known for simplicity. Used in web (Django, Flask), data science (pandas, NumPy), AI/ML (TensorFlow, PyTorch), automation. It has a large standard library and strong community support."),
    ("java", "Java is an object‑oriented, platform‑independent language. Used for enterprise applications, Android development, large‑scale systems. Features: JVM, garbage collection, strong typing, multithreading."),
    ("c++", "C++ extends C with object‑oriented features. Used in game development, system software, embedded systems, performance‑critical apps. It provides low‑level memory manipulation and high performance."),
    ("javascript", "JavaScript is the language of the web. It enables interactive web pages and is used on both client‑side and server‑side (Node.js). Frameworks: React, Angular, Vue. It's event‑driven and supports asynchronous programming."),
    ("c#", "C# (C‑Sharp) is a modern object‑oriented language from Microsoft. Used for Windows applications, game development (Unity), and enterprise software. Features: LINQ, async/await, strong typing."),
    ("php", "PHP is a server‑side scripting language designed for web development. Powers many content management systems like WordPress, Joomla, Drupal. Easy to learn and integrates with databases."),
    ("swift", "Swift is Apple's language for iOS and macOS development. Fast, safe, expressive, replacing Objective‑C. Supports protocol‑oriented programming and modern syntax."),
    ("kotlin", "Kotlin is a modern JVM language that interoperates with Java. Officially supported for Android development, concise and safe. Reduces boilerplate code and avoids null pointer exceptions."),
    ("ruby", "Ruby is a dynamic, object‑oriented language known for elegant syntax. Popular with Ruby on Rails for web development. Emphasizes convention over configuration."),
    ("go", "Go (Golang) is a compiled language by Google, designed for concurrency and simplicity. Used in cloud services, networking, DevOps. Features goroutines for lightweight concurrency."),
    ("rust", "Rust is a systems language focused on safety and performance. Used for building reliable software, including operating systems and game engines. Guarantees memory safety without garbage collection."),
    ("typescript", "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. Adds static typing and modern features for large‑scale applications. Improves developer productivity and code maintainability."),
    ("c", "C is a procedural programming language developed by Dennis Ritchie. Used for system programming, embedded systems, operating systems. Provides low‑level access to memory and is highly efficient."),
    ("sql", "SQL (Structured Query Language) is used to manage relational databases. Allows querying, inserting, updating, and deleting data. Key commands: SELECT, INSERT, UPDATE, DELETE, JOIN, CREATE TABLE."),
    ("r", "R is a programming language for statistical computing and graphics. Widely used among statisticians and data miners for developing statistical software and data analysis."),
    ("perl", "Perl is a high‑level, interpreted language known for text processing capabilities. Used in system administration, web development, and network programming."),
    ("scala", "Scala combines object‑oriented and functional programming. Runs on the JVM and is used for building scalable applications, especially with Apache Spark."),
    ("dart", "Dart is a client‑optimized language for fast apps on any platform. Used with Flutter for building natively compiled applications for mobile, web, and desktop."),
    ("html", "HTML (HyperText Markup Language) is the standard markup language for creating web pages. Structures content with elements like headings, paragraphs, links, images, forms."),
    ("css", "CSS (Cascading Style Sheets) styles HTML elements. Controls layout, colors, fonts, and responsive design. Frameworks: Bootstrap, Tailwind. Preprocessors: Sass, Less."),
    ("bash", "Bash is a Unix shell and command language. Used for scripting and automating tasks in Linux/Unix environments."),
    ("powershell", "PowerShell is a task automation and configuration management framework from Microsoft, consisting of a command‑line shell and scripting language."),
    ("kotlin", "Kotlin is a modern JVM language that interoperates with Java. It's officially supported for Android development and is concise and safe. It reduces boilerplate code and avoids null pointer exceptions."),
    ("swift", "Swift is Apple's language for iOS and macOS development. It's fast, safe, and expressive, replacing Objective‑C. It supports protocol‑oriented programming and has modern syntax."),
    ("ruby", "Ruby is a dynamic, object‑oriented language known for its elegant syntax. It's popular with the Ruby on Rails framework for web development. It emphasizes convention over configuration."),
    ("go", "Go (Golang) is a compiled language by Google, designed for concurrency and simplicity. It's used in cloud services, networking, and DevOps tools. It has goroutines for lightweight concurrency."),
    ("rust", "Rust is a systems language focused on safety and performance. It's used for building reliable software, including operating systems and game engines. It guarantees memory safety without garbage collection."),
    ("typescript", "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. It adds static typing and modern features for large‑scale applications. It improves developer productivity and code maintainability."),
    ("dart", "Dart is a client‑optimized language for fast apps on any platform. It is used with the Flutter framework for building natively compiled applications for mobile, web, and desktop."),
]

for lang, desc in languages:
    keywords = [lang, f"{lang} language", f"what is {lang}", f"explain {lang}", f"tell me about {lang}", f"learn {lang}"]
    add_entry(keywords, desc)

# ========== Data Structures ==========
ds_list = [
    ("data structures", "Data structures are ways to organize and store data efficiently. Common ones: arrays, linked lists, stacks, queues, trees, graphs, hash tables. Choosing the right data structure is crucial for algorithm performance."),
    ("array", "An array is a collection of elements stored at contiguous memory locations. It allows random access via index. Used for storing lists of data. Time complexity: access O(1), search O(n), insertion/deletion O(n)."),
    ("linked list", "A linked list is a linear data structure where elements (nodes) are linked using pointers. Types: singly, doubly, circular. It allows efficient insertion/deletion O(1) at known position but slow access O(n)."),
    ("stack", "A stack is a LIFO (Last In First Out) data structure. Operations: push (add), pop (remove), peek (top). Used in function calls, expression evaluation, undo operations, and backtracking."),
    ("queue", "A queue is a FIFO (First In First Out) data structure. Operations: enqueue (add), dequeue (remove). Used in scheduling, breadth‑first search, and task management. Variants: circular queue, priority queue, deque."),
    ("tree", "A tree is a hierarchical data structure with nodes connected by edges. Binary trees, binary search trees, AVL trees, B‑trees, heaps are common. Used in file systems, databases (indexing), HTML DOM, and decision trees."),
    ("binary tree", "A binary tree is a tree where each node has at most two children. Types: full, complete, perfect, balanced. Traversals: inorder, preorder, postorder, level‑order."),
    ("binary search tree", "A binary search tree (BST) is a binary tree where left child < parent < right child. It allows efficient search, insertion, deletion O(log n) on average. Balanced BSTs (AVL, Red‑Black) maintain O(log n) worst‑case."),
    ("graph", "A graph consists of vertices and edges. It can be directed or undirected, weighted or unweighted. Used in social networks, maps, recommendation systems. Algorithms: BFS, DFS, Dijkstra, A*, Bellman‑Ford, Floyd‑Warshall."),
    ("hash table", "A hash table (or hash map) stores key‑value pairs. It uses a hash function to compute an index. Provides O(1) average lookup, insertion, deletion. Used in databases, caches, dictionaries. Collision resolution: chaining, open addressing."),
    ("heap", "A heap is a specialized tree‑based data structure that satisfies the heap property. Max‑heap: parent >= children; Min‑heap: parent <= children. Used in priority queues, heap sort."),
    ("trie", "A trie is a tree‑like data structure for storing strings. Each node represents a common prefix. Used in autocomplete, spell checkers, IP routing."),
]

for topic, desc in ds_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}", f"tell me about {topic}"], desc)

# ========== Algorithms ==========
algos_list = [
    ("algorithms", "Algorithms are step‑by‑step procedures for solving problems. Key concepts: sorting (quick sort, merge sort), searching (binary search), recursion, dynamic programming, and complexity analysis (Big O notation)."),
    ("sorting algorithms", "Sorting arranges data in order. Common algorithms: Bubble Sort (simple but slow), Quick Sort (fast average), Merge Sort (stable, O(n log n)), Heap Sort (in‑place), Insertion Sort (good for small data). Time complexities vary."),
    ("quick sort", "Quick sort is a divide‑and‑conquer algorithm. It picks a pivot and partitions the array around it. Average time O(n log n), worst‑case O(n²) but can be avoided with good pivot selection. In‑place but not stable."),
    ("merge sort", "Merge sort is a divide‑and‑conquer algorithm that divides the array into halves, sorts them, and merges. Time O(n log n) always, stable, but requires O(n) extra space."),
    ("binary search", "Binary search finds the position of a target value in a sorted array. It compares the target to the middle element and eliminates half. Time O(log n). Requires sorted data."),
    ("dynamic programming", "Dynamic programming solves complex problems by breaking them into simpler subproblems and storing results to avoid recomputation. Used in optimization problems like Fibonacci, knapsack, shortest path."),
    ("recursion", "Recursion is a technique where a function calls itself to solve smaller instances. It requires a base case and recursive case. Used in tree traversals, divide‑and‑conquer algorithms."),
    ("big o notation", "Big O notation describes the upper bound of an algorithm's time or space complexity. Examples: O(1) constant, O(log n) logarithmic, O(n) linear, O(n²) quadratic, O(2^n) exponential."),
    ("greedy algorithm", "Greedy algorithms make the locally optimal choice at each stage, hoping to find a global optimum. Examples: Huffman coding, Dijkstra's algorithm, activity selection."),
    ("backtracking", "Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally and removing solutions that fail constraints. Examples: N‑Queens, Sudoku, maze solving."),
    ("divide and conquer", "Divide and conquer algorithms work by recursively breaking down a problem into subproblems, solving them, and combining results. Examples: merge sort, quick sort, binary search."),
]

for topic, desc in algos_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Operating Systems ==========
os_list = [
    ("operating system", "An operating system (OS) manages computer hardware and software. Examples: Windows, macOS, Linux, Android. Key functions: process management, memory management, file systems, device management, security."),
    ("process management", "Process management involves creating, scheduling, and terminating processes. Concepts: PCB, states (new, ready, running, waiting, terminated), context switching, IPC (pipes, message queues, shared memory)."),
    ("cpu scheduling", "CPU scheduling decides which process gets the CPU. Algorithms: FCFS, SJF, Round Robin, Priority. Goals: maximize throughput, minimize response time, avoid starvation."),
    ("memory management", "Memory management allocates and deallocates memory. Techniques: paging, segmentation, virtual memory, demand paging. Concepts: logical vs physical address, MMU, page faults, thrashing."),
    ("file system", "A file system controls how data is stored and retrieved. Examples: NTFS, FAT32, ext4, APFS. It organizes files into directories, manages metadata, and ensures data integrity."),
    ("linux", "Linux is an open‑source OS kernel. Distributions: Ubuntu, Fedora, CentOS, Debian. Widely used in servers, development, and embedded systems. It follows Unix philosophy and supports multitasking, multiuser."),
    ("windows", "Windows is a popular OS from Microsoft with a graphical interface. Versions: Windows 10, 11, Server. It supports a wide range of software and hardware, with features like task manager, registry, and PowerShell."),
    ("macos", "macOS is Apple's OS for Mac computers. Known for its Unix‑based architecture and seamless integration with Apple devices. It has a sleek UI and is popular among developers and creatives."),
    ("android", "Android is a mobile operating system based on Linux. It's developed by Google and used in smartphones, tablets, and smart devices. It has a large app ecosystem and customizable interface."),
    ("ios", "iOS is Apple's mobile operating system for iPhones and iPads. Known for its security, smooth performance, and integration with Apple services."),
    ("deadlock", "Deadlock is a situation where two or more processes are unable to proceed because each is waiting for resources held by the other. Conditions: mutual exclusion, hold and wait, no preemption, circular wait. Solutions: prevention, avoidance, detection, recovery."),
]

for topic, desc in os_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Computer Networks ==========
net_list = [
    ("computer networks", "Computer networks connect multiple devices to share resources and data. Types: LAN, WAN, MAN. Key concepts: IP addresses, protocols, OSI model, TCP/IP, routing, switching."),
    ("osi model", "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application. It standardizes network communication and helps in troubleshooting."),
    ("tcp/ip", "TCP/IP is the fundamental protocol suite for the internet. TCP ensures reliable delivery, IP handles addressing and routing. It has 4 layers: Application, Transport, Internet, Network Access."),
    ("http", "HTTP (Hypertext Transfer Protocol) is used for web communication. HTTPS adds encryption. Methods: GET, POST, PUT, DELETE, PATCH. It is stateless and works over TCP."),
    ("dns", "DNS (Domain Name System) translates domain names (like google.com) into IP addresses. It is a hierarchical system with root servers, TLD servers, and authoritative name servers."),
    ("ip address", "An IP address is a unique identifier for a device on a network. IPv4 uses 32‑bit addresses (e.g., 192.168.1.1), IPv6 uses 128‑bit. It can be static or dynamic."),
    ("firewall", "A firewall monitors and controls incoming/outgoing network traffic based on security rules. It acts as a barrier between trusted and untrusted networks. Types: packet‑filtering, stateful, application‑layer."),
    ("router", "A router forwards data packets between computer networks. It uses routing tables and protocols (RIP, OSPF, BGP) to determine the best path."),
    ("switch", "A switch connects devices on a local area network (LAN) and uses MAC addresses to forward data to the correct destination."),
    ("vpn", "VPN (Virtual Private Network) extends a private network across a public network, enabling users to send and receive data as if their devices were directly connected to the private network. It provides privacy and security."),
    ("ethernet", "Ethernet is a family of wired networking technologies commonly used in LANs. It defines physical and data link layer specifications."),
    ("wifi", "Wi‑Fi is a wireless networking technology that uses radio waves to provide high‑speed internet and network connections."),
]

for topic, desc in net_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Databases ==========
db_list = [
    ("database management", "Database management involves storing, organizing, and retrieving data. DBMS (Database Management System) software like MySQL, Oracle, SQL Server. It ensures data integrity, security, and concurrency."),
    ("sql", "SQL (Structured Query Language) is used to manage relational databases. Commands: SELECT, INSERT, UPDATE, DELETE, JOIN, CREATE TABLE, ALTER, DROP. It also includes subqueries, views, and transactions."),
    ("nosql", "NoSQL databases are non‑relational and handle unstructured data. Types: document (MongoDB), key‑value (Redis), column‑family (Cassandra), graph (Neo4j). They are scalable and flexible for big data."),
    ("acid", "ACID properties ensure reliable database transactions: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions don't interfere), Durability (committed changes persist)."),
    ("normalization", "Normalization organizes data to reduce redundancy and improve integrity. Normal forms: 1NF (atomic values), 2NF (remove partial dependencies), 3NF (remove transitive dependencies), BCNF (stronger)."),
    ("mysql", "MySQL is an open‑source relational database management system. It uses SQL and is widely used for web applications (LAMP stack). It supports ACID transactions, stored procedures, triggers."),
    ("mongodb", "MongoDB is a NoSQL document database. It stores data in JSON‑like documents with dynamic schemas. It is scalable, high‑performance, and used for modern applications."),
    ("postgresql", "PostgreSQL is a powerful, open‑source object‑relational database system. It supports advanced data types, full‑text search, and extensibility."),
    ("oracle", "Oracle Database is a multi‑model database management system commonly used for enterprise applications. It offers robust features, scalability, and security."),
    ("redis", "Redis is an in‑memory data structure store, used as a database, cache, and message broker. It supports data structures like strings, hashes, lists, sets."),
    ("cassandra", "Apache Cassandra is a distributed NoSQL database designed for handling large amounts of data across many commodity servers, providing high availability with no single point of failure."),
    ("neo4j", "Neo4j is a graph database that stores data in nodes and relationships. It's used for applications like social networks, recommendation engines, and fraud detection."),
]

for topic, desc in db_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== AI & ML (additional short entries) ==========
ai_ml_list = [
    ("artificial intelligence", "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes learning, reasoning, perception, and problem‑solving. Subfields: ML, NLP, computer vision, robotics."),
    ("machine learning", "Machine Learning (ML) is a subset of AI where systems learn from data. Types: supervised (labeled data), unsupervised (unlabeled), reinforcement (reward‑based). Algorithms: linear regression, decision trees, SVM, neural networks."),
    ("deep learning", "Deep Learning uses neural networks with many layers. It powers image recognition, speech recognition, and natural language processing. Frameworks: TensorFlow, PyTorch, Keras."),
    ("neural networks", "Neural networks are computing systems inspired by biological brains. They consist of layers of interconnected nodes (neurons). Used in deep learning for complex pattern recognition. Types: CNN, RNN, GAN."),
    ("natural language processing", "NLP enables computers to understand and generate human language. Applications: chatbots, translation, sentiment analysis. Techniques: tokenization, word embeddings (Word2Vec, BERT), transformers."),
    ("computer vision", "Computer vision enables machines to interpret visual data. Used in facial recognition, object detection, medical imaging. Libraries: OpenCV, YOLO, TensorFlow Object Detection."),
    ("supervised learning", "Supervised learning uses labeled data to train models. Examples: classification (spam detection), regression (price prediction). Algorithms: linear regression, logistic regression, SVM, random forest."),
    ("unsupervised learning", "Unsupervised learning finds patterns in unlabeled data. Examples: clustering (customer segmentation), association (market basket analysis). Algorithms: K‑means, hierarchical clustering, Apriori."),
    ("reinforcement learning", "Reinforcement learning involves an agent learning by interacting with an environment, receiving rewards or penalties. Used in game playing, robotics, self‑driving cars."),
    ("nlp", "Natural Language Processing (NLP) is a field of AI that gives machines the ability to read, understand, and derive meaning from human languages."),
    ("chatbot", "A chatbot is a software application used to conduct an on‑line chat conversation via text or text‑to‑speech, in lieu of providing direct contact with a live human agent."),
]

for topic, desc in ai_ml_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Cybersecurity (additional short) ==========
cyber_list = [
    ("cybersecurity", "Cybersecurity protects systems, networks, and data from digital attacks. Key areas: network security, application security, information security, incident response, disaster recovery."),
    ("encryption", "Encryption converts data into a coded form to prevent unauthorized access. Symmetric (AES, DES) uses same key; asymmetric (RSA, ECC) uses public/private keys. Used in HTTPS, secure messaging, file encryption."),
    ("ethical hacking", "Ethical hacking (penetration testing) simulates attacks to identify vulnerabilities. Ethical hackers use tools like Metasploit, Nmap, Wireshark to test systems and report findings."),
    ("malware", "Malware (malicious software) includes viruses, worms, trojans, ransomware, spyware, adware. It can steal data, damage systems, or encrypt files. Protection: antivirus, firewalls, safe browsing."),
    ("phishing", "Phishing is a social engineering attack where attackers impersonate legitimate entities to trick users into revealing sensitive information. Awareness and email filters help prevent."),
    ("ransomware", "Ransomware is a type of malware that encrypts the victim's files and demands a ransom for decryption. Prevention: regular backups, security updates, user training."),
    ("firewall", "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies."),
    ("ids", "Intrusion Detection System (IDS) monitors network traffic for suspicious activity and alerts administrators. Types: network‑based (NIDS), host‑based (HIDS)."),
    ("ips", "Intrusion Prevention System (IPS) is similar to IDS but also takes action to block or prevent detected threats."),
]

for topic, desc in cyber_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Cloud Computing (additional short) ==========
cloud_list = [
    ("cloud computing", "Cloud computing delivers computing services over the internet. Models: IaaS, PaaS, SaaS. Providers: AWS, Azure, Google Cloud. Benefits: scalability, cost‑efficiency, reliability."),
    ("aws", "Amazon Web Services (AWS) is a comprehensive cloud platform offering compute (EC2), storage (S3), databases (RDS), and more. It has global infrastructure and pay‑as‑you‑go pricing."),
    ("azure", "Microsoft Azure is a cloud platform with services for computing, analytics, storage, and networking. Integrates well with Microsoft products. Supports hybrid cloud and AI services."),
    ("google cloud", "Google Cloud Platform (GCP) offers cloud services including Compute Engine, App Engine, BigQuery, and Kubernetes. It is strong in data analytics and machine learning."),
    ("docker", "Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, portable, and consistent across environments. Docker images are built from Dockerfiles."),
    ("kubernetes", "Kubernetes (K8s) is an open‑source system for automating deployment, scaling, and management of containerized applications. It groups containers into pods and manages clusters."),
    ("serverless", "Serverless computing allows developers to build and run applications without managing servers. The cloud provider dynamically manages the allocation of resources. Examples: AWS Lambda, Azure Functions."),
    ("iaas", "Infrastructure as a Service (IaaS) provides virtualized computing resources over the internet. Users can rent virtual machines, storage, and networks. Examples: AWS EC2, Google Compute Engine."),
    ("paas", "Platform as a Service (PaaS) provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining infrastructure. Examples: Heroku, Google App Engine."),
    ("saas", "Software as a Service (SaaS) delivers software applications over the internet on a subscription basis. Examples: Google Workspace, Salesforce, Microsoft 365."),
]

for topic, desc in cloud_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Software Engineering (additional short) ==========
se_list = [
    ("software engineering", "Software engineering applies engineering principles to software development. It includes requirements analysis, design, implementation, testing, and maintenance. Methodologies: Agile, Waterfall, DevOps."),
    ("software development life cycle", "SDLC is a process for planning, creating, testing, and deploying software. Phases: Requirement Analysis, Design, Implementation, Testing, Deployment, Maintenance. Models: Waterfall, Agile, Spiral, V‑model."),
    ("agile", "Agile is an iterative approach to software development that emphasizes flexibility, collaboration, and customer feedback. Scrum and Kanban are popular Agile frameworks. It delivers working software in short sprints."),
    ("scrum", "Scrum is an Agile framework with roles (Product Owner, Scrum Master, Development Team), events (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Increment)."),
    ("devops", "DevOps is a culture and set of practices that combine development (Dev) and IT operations (Ops). It aims to shorten the development lifecycle and provide continuous delivery. Tools: Jenkins, Git, Docker, Kubernetes."),
    ("version control", "Version control systems track changes to code over time. Git is the most popular, with platforms like GitHub, GitLab. Commands: init, add, commit, push, pull, branch, merge."),
    ("testing", "Software testing ensures quality. Types: unit testing (individual components), integration testing (combined modules), system testing (whole system), acceptance testing (user requirements). Automated testing tools: JUnit, Selenium, pytest."),
    ("object oriented programming", "OOP is a programming paradigm based on objects containing data and methods. Key concepts: encapsulation, inheritance, polymorphism, abstraction. Languages: Java, C++, Python, C#."),
    ("oop concepts", "Four main OOP concepts: Encapsulation (bundling data and methods), Inheritance (creating new classes from existing ones), Polymorphism (same interface for different data types), Abstraction (hiding complexity)."),
    ("system design", "System design involves defining architecture, components, modules, and data to satisfy requirements. It includes high‑level design (HLD) and low‑level design (LLD). Key considerations: scalability, reliability, performance."),
    ("apis", "API (Application Programming Interface) allows software applications to communicate. REST, GraphQL, SOAP are common. APIs expose endpoints with methods (GET, POST) and return data (JSON, XML)."),
    ("git", "Git is a distributed version control system. Commands: clone, add, commit, push, pull, branch, merge. Platforms: GitHub, GitLab, Bitbucket. It enables collaboration and code history tracking."),
    ("jenkins", "Jenkins is an open‑source automation server used for continuous integration and continuous delivery (CI/CD). It helps automate building, testing, and deploying software."),
    ("jira", "Jira is a project management tool used for issue tracking and agile project management. It's popular among software development teams."),
]

for topic, desc in se_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Web Development ==========
web_list = [
    ("web development", "Web development involves building websites and web applications. Front‑end (client‑side) and back‑end (server‑side). Technologies: HTML, CSS, JavaScript, frameworks, databases, APIs."),
    ("html", "HTML (HyperText Markup Language) is the standard markup language for creating web pages. It structures content with elements like headings, paragraphs, links, images, forms."),
    ("css", "CSS (Cascading Style Sheets) styles HTML elements. It controls layout, colors, fonts, and responsive design. Frameworks: Bootstrap, Tailwind. Preprocessors: Sass, Less."),
    ("javascript", "JavaScript is the programming language of the web. It adds interactivity to web pages. It runs in browsers and on servers (Node.js). Libraries: jQuery, React, Angular, Vue."),
    ("frontend development", "Front‑end development focuses on the user interface. Languages: HTML, CSS, JavaScript. Frameworks: React, Angular, Vue. Tools: npm, webpack, Babel."),
    ("backend development", "Back‑end development handles server‑side logic, databases, and APIs. Languages: Python (Django, Flask), JavaScript (Node.js), Java (Spring), PHP (Laravel), Ruby (Rails). It manages authentication, data processing."),
    ("full stack development", "Full stack development involves both front‑end and back‑end. A full stack developer can build entire web applications. Popular stacks: MERN (MongoDB, Express, React, Node), MEAN (MongoDB, Express, Angular, Node), LAMP (Linux, Apache, MySQL, PHP)."),
    ("responsive design", "Responsive design ensures websites look good on all devices (desktop, tablet, mobile). Techniques: fluid grids, flexible images, media queries. Frameworks like Bootstrap make it easier."),
    ("react", "React is a JavaScript library for building user interfaces. Developed by Facebook, it allows building reusable UI components and efficiently updating the DOM."),
    ("angular", "Angular is a TypeScript‑based web application framework developed by Google. It provides a comprehensive solution for building client‑side applications."),
    ("vue", "Vue.js is a progressive JavaScript framework for building user interfaces. It is designed to be incrementally adoptable and focuses on the view layer."),
    ("nodejs", "Node.js is a JavaScript runtime built on Chrome's V8 engine. It allows running JavaScript on the server‑side, enabling full‑stack JavaScript development."),
    ("django", "Django is a high‑level Python web framework that encourages rapid development and clean, pragmatic design. It includes an ORM, admin interface, and authentication."),
    ("flask", "Flask is a lightweight WSGI web application framework in Python. It is designed to be simple and extensible."),
    ("spring", "Spring is a powerful Java framework for building enterprise applications. It provides comprehensive infrastructure support for developing Java applications."),
]

for topic, desc in web_list:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Career Paths ==========
career_list = [
    ("software developer career", "Software developers design, code, and test software. Skills: programming languages (Java, Python, C#), problem‑solving, teamwork. Path: learn languages, build projects, contribute to open source, prepare for interviews. Certifications: Oracle Certified Professional, AWS Developer."),
    ("data science career", "Data scientists analyze data to extract insights. Skills: Python, R, SQL, statistics, machine learning. Path: learn tools (pandas, scikit‑learn), work on projects, get certifications (IBM Data Science, Google Data Analytics). Roles: Data Analyst, Data Engineer, ML Engineer."),
    ("ai engineer career", "AI engineers build AI models and systems. Skills: machine learning, deep learning, Python, TensorFlow, PyTorch. Path: master math/statistics, take online courses, contribute to AI projects. Certifications: TensorFlow Developer Certificate, AWS AI."),
    ("cybersecurity career", "Cybersecurity professionals protect systems. Roles: Security Analyst, Penetration Tester, Security Architect. Skills: networking, OS, scripting, risk assessment. Certifications: CEH, CISSP, CompTIA Security+."),
    ("cloud engineer career", "Cloud engineers manage cloud infrastructure. Skills: AWS/Azure/GCP, automation (Terraform), containerization (Docker, Kubernetes). Path: get cloud certifications, build projects. Certifications: AWS Solutions Architect, Azure Administrator."),
    ("devops career", "DevOps engineers bridge development and operations. Skills: scripting (Python, Bash), CI/CD tools, containerization, cloud platforms. Certifications: AWS DevOps Engineer, Docker Certified Associate."),
    ("web developer career", "Web developers build websites and web apps. Front‑end: HTML, CSS, JavaScript. Back‑end: Node.js, Python, PHP. Full‑stack: both. Build a portfolio, learn frameworks, and stay updated."),
    ("how to become a software developer", "1. Choose a programming language (Python, Java). 2. Learn fundamentals (data structures, algorithms). 3. Build projects (web apps, tools). 4. Contribute to open source. 5. Prepare for interviews (LeetCode). 6. Apply for internships/jobs. Continuous learning is key."),
]

for topic, desc in career_list:
    add_entry([topic, topic.replace("career", "career path"), f"how to become a {topic.split()[0]}"], desc)

# ========== BCA Additional Topics ==========
bca_extra = [
    ("bca subjects", "BCA subjects include: Programming languages (C, C++, Java, Python), Data Structures, Database Management, Computer Networks, Operating Systems, Software Engineering, Web Development, Mathematics, and Cloud Computing basics. The syllabus is spread over 6 semesters, with each semester covering 5‑6 subjects."),
    ("bca eligibility", "Eligibility for BCA: Candidates must have completed 10+2 (or equivalent) from a recognized board with Mathematics or Computer Science as a subject. Minimum aggregate marks typically range from 45% to 50% (relaxation for reserved categories). Some universities also require English as a subject."),
    ("bca duration", "BCA is a 3‑year undergraduate program divided into 6 semesters. Some institutes offer part‑time or distance learning options, but the standard duration is 3 years."),
    ("bca programming languages", "In BCA, students typically learn: C, C++, Java, Python, JavaScript, and sometimes PHP, SQL, and HTML/CSS. These languages cover procedural, object‑oriented, and web development paradigms."),
    ("bca skills", "Skills developed during BCA: programming proficiency, problem‑solving, database management, understanding of networking, software development lifecycle, teamwork, and project management. Students also gain analytical and communication skills."),
    ("jobs after bca", "After BCA, common job roles include: Software Developer, Web Developer, Data Analyst, System Administrator, Network Engineer, Cybersecurity Analyst, Mobile App Developer, Cloud Engineer, DevOps Engineer, and Technical Support. Many graduates also pursue higher studies like MCA or MBA."),
    ("bca salary", "Average salary for BCA freshers in India ranges from ₹2.5 to 5 LPA. With experience and certifications, it can go up to ₹10‑15 LPA or more. Salaries vary based on skills, company, and location."),
    ("bca future scope", "Future scope after BCA is bright. Graduates can work in IT companies, startups, government organizations, or as freelancers. With additional certifications in AI, data science, cloud, or cybersecurity, they can advance to specialized roles. Higher studies like MCA open doors to research and academia."),
    ("higher studies after bca", "Popular higher studies after BCA: MCA (Master of Computer Applications) – 2 years, deepens computer knowledge; MBA in IT – management roles; MSc in Computer Science; Data Science or AI certifications; Cloud certifications (AWS, Azure)."),
    ("bca vs cs", "BCA is a professional undergraduate degree focused on applications and software development, while Computer Science is an academic discipline covering theory, algorithms, and systems. BCA is more industry‑oriented; CS is broader and often pursued as B.Sc. CS or B.E./B.Tech. Both lead to careers in IT."),
    ("bca freelancing", "BCA graduates can freelance in web development, mobile app development, software testing, technical writing, and digital marketing. Platforms like Upwork, Fiverr, and Freelancer offer opportunities. Building a strong portfolio is key."),
    ("bca startup", "With programming and business skills, BCA graduates can launch startups in software development, e‑commerce, ed‑tech, or IT services. Incubators and government schemes like Startup India provide support."),
    ("bca industry demand", "Demand for BCA graduates is high in IT companies, banks, government sectors, and multinational corporations. Roles in software development, data analytics, and cloud computing are particularly in demand."),
    ("bca projects", "BCA projects help apply theoretical knowledge. Ideas: Library Management System, Online Quiz Portal, E‑commerce Website, Chatbot, Weather App, Student Database, Hospital Management System. Use languages like Java, Python, PHP, and databases like MySQL."),
    ("bca internships", "BCA students can intern as software developers, web developers, data analysts, or IT support. Internships provide industry exposure and improve employability. Platforms like Internshala, LinkedIn, and company career pages list opportunities."),
]

for topic, desc in bca_extra:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Computer Science General ==========
cs_general = [
    ("history of computers", "The history of computers dates back to the abacus and mechanical calculators. Key milestones: Charles Babbage's Analytical Engine (1837), ENIAC (1945) – first electronic general‑purpose computer, invention of transistors (1947), integrated circuits (1958), microprocessors (1971), personal computers (1980s), internet (1990s), and the era of AI and cloud computing today."),
    ("computer science career", "Computer Science careers include: Software Engineer, Data Scientist, AI/ML Engineer, Cybersecurity Analyst, Cloud Architect, DevOps Engineer, Game Developer, Mobile App Developer, IT Consultant, and Research Scientist. Opportunities exist in tech companies, finance, healthcare, and government."),
    ("computer science future scope", "The future of Computer Science is promising with emerging fields like quantum computing, edge computing, AI ethics, blockchain, IoT, and bioinformatics. CS professionals will continue to be in high demand as technology integrates into every aspect of life."),
]

for topic, desc in cs_general:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

# ========== Additional / Miscellaneous ==========
extra_topics = [
    ("blockchain", "Blockchain is a decentralized, distributed ledger technology. It records transactions across many computers so that the record cannot be altered retroactively. Used in cryptocurrencies (Bitcoin), smart contracts, supply chain, voting."),
    ("iot", "Internet of Things (IoT) connects physical devices to the internet. Applications: smart homes, wearables, industrial automation, healthcare monitoring. Devices collect and exchange data using sensors and connectivity."),
    ("big data", "Big data refers to extremely large datasets that require specialized tools. Technologies: Hadoop, Spark, Kafka. Characteristics: volume, velocity, variety. Used in analytics, machine learning, business intelligence."),
    ("data science", "Data science combines statistics, programming, and domain knowledge to extract insights from data. It involves data cleaning, exploration, modeling, and visualization. Tools: Python (pandas, NumPy, scikit‑learn), R, SQL."),
    ("quantum computing", "Quantum computing uses quantum bits (qubits) to perform computations. It leverages superposition and entanglement to solve problems faster than classical computers. Potential applications: cryptography, optimization, drug discovery."),
    ("compiler design", "Compiler design involves translating high‑level language to machine code. Phases: lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, code generation. Tools: Lex, Yacc."),
    ("distributed systems", "Distributed systems consist of multiple computers that appear as a single coherent system. They communicate over a network and coordinate via protocols. Examples: cloud computing, peer‑to‑peer networks, distributed databases."),
    ("computer architecture", "Computer architecture describes the design of computer systems. It includes CPU design, instruction set architecture, memory hierarchy, I/O. Concepts: pipelining, caching, parallelism."),
    ("human computer interaction", "HCI studies how people interact with computers. It focuses on usability, user experience, interface design. Principles: visibility, feedback, consistency, affordance."),
    ("software testing", "Software testing verifies that software meets requirements and finds defects. Types: manual, automated, black‑box, white‑box, performance, security. Tools: Selenium, JUnit, TestNG."),
    ("rest api", "REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP methods (GET, POST, PUT, DELETE) and are stateless."),
    ("graphql", "GraphQL is a query language for APIs that allows clients to request exactly the data they need. It provides a more efficient and flexible alternative to REST."),
    ("microservices", "Microservices architecture structures an application as a collection of small, loosely coupled services. Each service is independently deployable and scalable."),
    ("serverless", "Serverless computing allows developers to run code without provisioning servers. The cloud provider manages the infrastructure. Examples: AWS Lambda, Azure Functions."),
    ("ci/cd", "CI/CD (Continuous Integration/Continuous Delivery) is a practice that automates the integration and delivery of code changes. Tools: Jenkins, GitLab CI, CircleCI."),
    ("terraform", "Terraform is an infrastructure as code tool that allows you to define and provision infrastructure using a declarative configuration language."),
    ("ansible", "Ansible is an open‑source automation tool for configuration management, application deployment, and task automation. It uses YAML playbooks."),
    ("prometheus", "Prometheus is an open‑source monitoring and alerting toolkit commonly used in cloud‑native environments."),
    ("grafana", "Grafana is an open‑source analytics and visualization platform that integrates with various data sources."),
    ("elasticsearch", "Elasticsearch is a distributed search and analytics engine based on Lucene. It's used for log analytics, full‑text search, and more."),
    ("kafka", "Apache Kafka is a distributed event streaming platform used for building real‑time data pipelines and streaming applications."),
    ("spark", "Apache Spark is a unified analytics engine for large‑scale data processing. It supports SQL, streaming, machine learning, and graph processing."),
    ("hadoop", "Apache Hadoop is a framework for distributed storage and processing of big data using the MapReduce programming model."),
    ("flink", "Apache Flink is a stream processing framework for real‑time data processing."),
]

for topic, desc in extra_topics:
    add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)

    # -------------------- Response Engine --------------------
def get_bot_response(user_input: str) -> str:
    """Main entry point for bot responses."""
    try:
        # First try the knowledge base search
        answer = kb.search(user_input)
        return answer
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"

# -------------------- Navigation Functions --------------------
def go_to_chat():
    st.session_state.page = "chat"

def go_to_landing():
    st.session_state.page = "landing"

# -------------------- Custom CSS (Ultra‑modern glassmorphism with animations) --------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Animated gradient background with floating particles */
    .stApp {
        background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1b3b4f);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        position: relative;
        overflow-x: hidden;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating orbs / particles */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 0%, transparent 20%),
            radial-gradient(circle at 80% 70%, rgba(255,255,255,0.1) 0%, transparent 25%),
            radial-gradient(circle at 40% 80%, rgba(255,255,255,0.12) 0%, transparent 22%),
            radial-gradient(circle at 90% 20%, rgba(255,255,255,0.08) 0%, transparent 30%),
            radial-gradient(circle at 10% 60%, rgba(255,255,255,0.1) 0%, transparent 28%);
        animation: floatOrbs 35s linear infinite;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes floatOrbs {
        0% { transform: translate(0, 0) scale(1); opacity: 0.5; }
        33% { transform: translate(2%, 3%) scale(1.05); opacity: 0.7; }
        66% { transform: translate(-1%, 2%) scale(0.98); opacity: 0.6; }
        100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
    }

    .stApp > div {
        position: relative;
        z-index: 5;
    }

    /* Glassmorphism base */
    .glass {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }

    /* Fade-in animation */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeInUp 0.8s ease forwards;
    }

    /* Hero card */
    .hero-card {
        max-width: 950px;
        width: 92%;
        margin: 2rem auto;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 70px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
        text-align: center;
        transition: all 0.5s;
        animation: fadeInUp 1s ease;
        position: relative;
        z-index: 2;
    }

    .hero-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255,255,255,0.4);
        box-shadow: 0 50px 100px rgba(0,0,0,0.6);
    }

    /* Icon with glowing pulse */
    .icon-container {
        position: relative;
        width: 160px;
        height: 160px;
        margin: 0 auto 1.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .robot-icon {
        font-size: 7rem;
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 0 15px rgba(102,126,234,0.8));
    }
    .glow-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 140px;
        height: 140px;
        background: radial-gradient(circle,
            rgba(102,126,234,0.9) 0%,
            rgba(102,126,234,0.5) 40%,
            rgba(102,126,234,0.2) 65%,
            transparent 80%);
        border-radius: 50%;
        animation: pulseGlow 4s ease-out infinite;
        z-index: 1;
    }
    @keyframes pulseGlow {
        0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.9; }
        50% { transform: translate(-50%, -50%) scale(1.4); opacity: 0.4; }
        100% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.9; }
    }

    @keyframes neonGlow {
        from {
            text-shadow:
                0 0 5px #667eea,
                0 0 10px #667eea,
                0 0 20px #667eea,
                0 0 40px #764ba2,
                0 0 80px #764ba2;
        }
        to {
            text-shadow:
                0 0 10px #667eea,
                0 0 20px #667eea,
                0 0 40px #667eea,
                0 0 80px #764ba2,
                0 0 120px #764ba2;
        }
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #ffffff;
        animation: neonGlow 2.5s ease-in-out infinite alternate;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        color: rgba(255,255,255,0.9);
        margin: 1rem auto 1.5rem;
        max-width: 80%;
        line-height: 1.6;
    }

    .hero-credit {
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 1.5rem;
        text-shadow: 0 0 10px rgba(102,126,234,0.5);
    }
    .hero-meta {
        color: rgba(255,255,255,0.7);
        font-size: 1rem;
        font-weight: 400;
    }

    /* Stats row */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 2.5rem 0 4rem;
        flex-wrap: wrap;
        z-index: 2;
        position: relative;
    }
    .stat-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        padding: 2rem 3.5rem;
        border: 1px solid rgba(255,255,255,0.15);
        text-align: center;
        transition: all 0.4s;
        animation: fadeInUp 1.2s ease;
        min-width: 200px;
    }
    .stat-card:hover {
        transform: scale(1.08);
        border-color: rgba(255,255,255,0.4);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }
    .stat-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        line-height: 1.2;
        text-shadow: 0 0 20px rgba(255,255,255,0.4);
    }
    .stat-label {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.85);
    }

    /* Section titles */
    .section-title {
        text-align: center;
        color: white;
        font-size: 3.2rem;
        font-weight: 600;
        margin: 4rem 0 2.5rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.4);
        animation: fadeInUp 0.8s ease;
    }

    /* Feature cards grid */
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.5rem;
        max-width: 1300px;
        margin: 3rem auto;
        padding: 0 2rem;
        position: relative;
        z-index: 2;
    }
    .feature-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border-radius: 45px;
        padding: 2.5rem 2rem;
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.5s;
        animation: fadeInUp 1s ease;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(255,255,255,0.4);
        box-shadow: 0 35px 60px rgba(0,0,0,0.5);
    }
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }
    .card-title {
        font-size: 2rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
    }
    .card-desc {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        line-height: 1.6;
        flex: 1;
    }
    .topic-list {
        margin-top: 1.5rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        justify-content: center;
    }
    .topic-tag {
        background: rgba(255,255,255,0.15);
        border-radius: 40px;
        padding: 0.4rem 1.2rem;
        font-size: 0.85rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        transition: 0.2s;
    }
    .topic-tag:hover {
        background: rgba(255,255,255,0.25);
        transform: scale(1.05);
    }

    /* Popular topics chips */
    .chips-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        max-width: 1100px;
        margin: 2rem auto;
        position: relative;
        z-index: 2;
    }
    .chips-container .stButton button {
        background: rgba(255,255,255,0.12) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: white !important;
        padding: 0.9rem 2rem !important;
        border-radius: 60px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        box-shadow: none !important;
    }
    .chips-container .stButton button:hover {
        background: rgba(255,255,255,0.25) !important;
        transform: scale(1.05) !important;
        border-color: rgba(255,255,255,0.4) !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3) !important;
    }

    /* Launch button */
    .launch-btn-container {
        display: flex;
        justify-content: center;
        margin: 3rem 0 4rem;
        position: relative;
        z-index: 2;
    }
    .launch-btn-container .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        padding: 1.5rem 6rem !important;
        border: none !important;
        border-radius: 80px !important;
        box-shadow: 0 20px 40px rgba(102,126,234,0.5) !important;
        transition: all 0.5s !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        animation: pulseBtn 2.5s infinite;
    }
    .launch-btn-container .stButton button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 30px 60px rgba(102,126,234,0.8) !important;
    }
    @keyframes pulseBtn {
        0% { box-shadow: 0 0 0 0 rgba(102,126,234,0.7); }
        70% { box-shadow: 0 0 0 25px rgba(102,126,234,0); }
        100% { box-shadow: 0 0 0 0 rgba(102,126,234,0); }
    }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.5);
        padding: 2.5rem;
        font-size: 0.95rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 4rem;
    }

    /* Navigation bar for chat page */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 2rem;
    }

    /* Chat header */
    .chat-header {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(15px);
        border-radius: 60px;
        padding: 2.5rem;
        margin: 1.5rem auto 3rem;
        max-width: 850px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
        animation: fadeInUp 0.8s ease;
    }
    .chat-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.8rem;
        text-shadow: 0 0 15px rgba(102,126,234,0.5);
    }
    .chat-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1.3rem;
    }

    /* Message bubbles */
    .message {
        display: flex;
        margin-bottom: 2rem;
        animation: fadeInUp 0.5s ease;
    }
    .message.user {
        justify-content: flex-end;
    }
    .message.assistant {
        justify-content: flex-start;
    }
    .message-bubble {
        max-width: 70%;
        padding: 1.3rem 2rem;
        border-radius: 30px;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        word-wrap: break-word;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .message.user .message-bubble {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-bottom-right-radius: 5px;
    }
    .message.assistant .message-bubble {
        background: rgba(255,255,255,0.15);
        border-bottom-left-radius: 5px;
    }

    /* Suggestion buttons (chat page) */
    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        justify-content: center;
        max-width: 850px;
        margin: 2rem auto;
    }
    .suggestions-container .stButton button {
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        padding: 0.7rem 1.8rem !important;
        border-radius: 50px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s !important;
    }
    .suggestions-container .stButton button:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: scale(1.02);
        border-color: rgba(255,255,255,0.3) !important;
    }

    /* Chat input */
    .stChatInput {
        max-width: 750px;
        margin: 0 auto !important;
    }
    .stChatInput > div {
        border-radius: 60px !important;
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        transition: all 0.3s !important;
        padding: 0.8rem 1.5rem !important;
    }
    .stChatInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 5px rgba(102,126,234,0.2) !important;
    }
    .stChatInput input {
        color: white !important;
        font-size: 1.05rem !important;
    }
    .stChatInput input::placeholder {
        color: rgba(255,255,255,0.5) !important;
    }

    /* Override Streamlit buttons */
    div.stButton > button {
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 40px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: none !important;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: scale(1.02) !important;
        border-color: rgba(255,255,255,0.4) !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------- Landing Page --------------------
def render_landing():
    st.markdown("""
    <div class="hero-card fade-in">
        <div class="icon-container">
            <div class="glow-circle"></div>
            <div class="robot-icon">🤖</div>
        </div>
        <div class="hero-title">Secure AI Agent</div>
        <div class="hero-subtitle">Next‑Generation CS/BCA Academic Assistant</div>
        <div class="hero-credit">Created by Mirza Jaffar Ali Baig | Aims Degree College</div>
        <div class="hero-meta">Built with Python & Streamlit • Open Source</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-number">1500+</div>
            <div class="stat-label">Topics</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">Free</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>What I Can Help You With</h2>", unsafe_allow_html=True)

    cards = [
        ("💻", "Computer Science", "Algorithms, data structures, programming, OS, networks, and more.",
         ["Algorithms", "Data Structures", "Programming", "OS", "Networks"]),
        ("📚", "BCA & Academics", "Course structure, syllabus, subjects, academic guidance.",
         ["BCA Syllabus", "Subjects", "Projects", "Internships"]),
        ("🚀", "Career Guidance", "Jobs after BCA, software dev, data science, cybersecurity careers.",
         ["Software Developer", "Data Scientist", "AI Engineer", "Cloud Architect"]),
        ("🤖", "AI & Machine Learning", "Neural networks, deep learning, NLP, computer vision, AI ethics.",
         ["Neural Networks", "Deep Learning", "NLP", "Computer Vision"]),
        ("☁️", "Cloud & DevOps", "AWS, Azure, Docker, Kubernetes, CI/CD, infrastructure as code.",
         ["AWS", "Docker", "Kubernetes", "CI/CD"]),
        ("🔒", "Cybersecurity", "Encryption, network security, ethical hacking, risk management.",
         ["Encryption", "Firewalls", "Pen Testing", "Malware"]),
        ("🐍", "Programming Languages", "Python, Java, C++, JavaScript, and many more.",
         ["Python", "Java", "C++", "JavaScript"]),
        ("📊", "Data Science", "Statistics, visualization, machine learning, big data.",
         ["Pandas", "NumPy", "Scikit‑learn", "Spark"]),
    ]

    st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
    for icon, title, desc, topics in cards:
        topic_tags = ''.join([f'<span class="topic-tag">{t}</span>' for t in topics])
        st.markdown(f"""
        <div class="feature-card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
            <div class="topic-list">{topic_tags}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>Try Asking</h2>", unsafe_allow_html=True)
    popular_questions = [
        "What is BCA?",
        "Future scope of BCA",
        "Explain Data Structures",
        "Career in Cybersecurity",
        "AI vs Machine Learning",
        "How to become a Software Developer?",
        "What is Cloud Computing?",
        "Explain OOP concepts",
        "Jobs after BCA",
        "What is Python?",
    ]

    st.markdown("<div class='chips-container'>", unsafe_allow_html=True)
    for q in popular_questions:
        if st.button(q, key=f"chip_{q}"):
            st.session_state.pending_question = q
            go_to_chat()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='launch-btn-container'>", unsafe_allow_html=True)
    if st.button("🚀 Launch Secure AI", key="launch_big"):
        go_to_chat()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        © 2026 Secure AI Agent — CS/BCA Academic Assistant. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

    # -------------------- Chat Page --------------------
def render_chat():
    # Navigation bar
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("🏠 Home", key="home"):
            go_to_landing()
            st.rerun()
    with col3:
        if st.button("🧹 Clear Chat", key="clear"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your CS/BCA Academic Assistant. Ask me about programming, algorithms, career paths, or any computer science topic."}
            ]
            st.rerun()

    # Chat Header
    st.markdown("""
    <div class="chat-header">
        <h1>💬 CS/BCA Assistant</h1>
        <p>Ask me anything about Computer Science or BCA</p>
    </div>
    """, unsafe_allow_html=True)
    # Suggestion buttons (full set)
    suggestions = [
        "What is BCA?",
        "Future scope of BCA",
        "Explain Data Structures",
        "Career in Cybersecurity",
        "AI vs Machine Learning",
        "How to become a Software Developer?",
        "What is Cloud Computing?",
        "Explain OOP concepts",
        "Jobs after BCA",
        "What is Python?",
    ]
    st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
    for s in suggestions:
        if st.button(s, key=f"sugg_{s}"):
            st.session_state.messages.append({"role": "user", "content": s})
            with st.spinner("Thinking..."):
                time.sleep(0.8)  # simulate thinking
                response = get_bot_response(s)
                time.sleep(0.4)  # simulate typing
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    # Display messages
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f"""
        <div class="message {role_class}">
            <div class="message-bubble">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Handle pending question from landing page
    if st.session_state.pending_question:
        q = st.session_state.pending_question
        st.session_state.pending_question = None
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("Thinking..."):
            time.sleep(0.8)
            response = get_bot_response(q)
            time.sleep(0.4)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Chat input
    prompt = st.chat_input("Type your question here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            time.sleep(0.8)
            response = get_bot_response(prompt)
            time.sleep(0.4)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# -------------------- Main --------------------
if st.session_state.page == "landing":
    render_landing()
else:
    render_chat()