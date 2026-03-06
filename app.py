import streamlit as st
import re
import time

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Secure AI Agent - CS/BCA Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- Detailed Answers for Major Topics --------------------
def get_detailed_answer(topic):
    """Return a structured detailed answer for major topics."""
    topic = topic.lower().strip()
    
    if "bca" in topic or "bachelor of computer applications" in topic:
        return """
### BCA (Bachelor of Computer Applications)

#### 1. Introduction
BCA is a 3-year undergraduate degree that focuses on computer applications and software development. It equips students with programming skills, database management, networking basics, and software engineering principles. The course is designed to meet the growing demand for IT professionals.

#### 2. Course Duration
BCA is typically a 3-year program divided into 6 semesters. Some universities also offer part-time or distance learning options.

#### 3. Subjects in BCA
- **Programming Languages**: C, C++, Java, Python
- **Data Structures and Algorithms**
- **Database Management Systems (SQL, MongoDB)**
- **Computer Networks**
- **Operating Systems**
- **Software Engineering**
- **Web Development (HTML, CSS, JavaScript)**
- **Mathematics (Discrete Mathematics, Probability)**
- **Cloud Computing Basics**
- **Cyber Security Fundamentals**

#### 4. Programming Languages Learned
- **C** – Procedural programming, memory management
- **C++** – Object-oriented programming
- **Java** – Platform-independent, OOP, Android development
- **Python** – Versatile, used in web development, data science, AI
- **JavaScript** – Web development, interactive front-end

#### 5. Skills Students Learn
- Problem-solving and logical thinking
- Proficiency in multiple programming languages
- Database design and management
- Understanding of networking concepts
- Software development lifecycle (SDLC)
- Team collaboration and project management

#### 6. Career Opportunities After BCA
- **Software Developer** – Build applications using Java, Python, C#
- **Web Developer** – Create websites using HTML, CSS, JavaScript, frameworks
- **Data Analyst** – Analyze data using SQL, Excel, Python
- **System Administrator** – Manage servers and networks
- **Network Engineer** – Configure and maintain networks
- **Cybersecurity Analyst** – Protect systems from threats
- **Mobile App Developer** – Android/iOS development
- **Cloud Engineer** – Work with AWS, Azure, Google Cloud
- **DevOps Engineer** – Automate deployment and infrastructure

#### 7. Higher Studies Options
- **MCA (Master of Computer Applications)** – Advanced computer applications
- **MBA (Master of Business Administration)** – IT management
- **M.Sc. in Computer Science** – Research and academia
- **Data Science / AI certifications**
- **Cloud certifications** (AWS, Azure)

#### 8. Future Scope
The IT industry continues to grow rapidly. BCA graduates are in high demand for roles in software development, data science, cybersecurity, and cloud computing. With additional certifications and experience, they can advance to senior developer, architect, or managerial positions. Freelancing and startup opportunities are also abundant.

#### 9. Average Salary (India)
- **Entry-level**: ₹2.5 – 5 LPA
- **Mid-level (3-5 years)**: ₹6 – 12 LPA
- **Senior-level**: ₹15+ LPA (varies by skills and company)
"""
    
    elif "computer science" in topic or "cs" in topic:
        return """
### Computer Science – A Comprehensive Overview

#### 1. Introduction
Computer Science is the study of computers and computational systems. Unlike electrical and computer engineering, computer science deals with software and software systems; this includes their theory, design, development, and application. Principal areas of study include artificial intelligence, computer systems and networks, security, database systems, human-computer interaction, vision and graphics, numerical analysis, programming languages, software engineering, bioinformatics and theory of computing.

#### 2. Core Areas of Computer Science
- **Algorithms and Data Structures** – Foundation for efficient problem-solving
- **Computer Architecture** – Design of CPUs, memory, I/O
- **Operating Systems** – Management of hardware and software resources
- **Computer Networks** – Data communication, protocols, internet
- **Database Systems** – Storage, retrieval, and management of data
- **Software Engineering** – Methodologies for building reliable software
- **Artificial Intelligence** – Machine learning, robotics, natural language processing
- **Cybersecurity** – Protecting systems from attacks
- **Theory of Computation** – Automata, computability, complexity

#### 3. Programming Languages in Computer Science
- **Python** – General-purpose, AI/ML, data science
- **Java** – Enterprise applications, Android
- **C/C++** – System programming, game development
- **JavaScript** – Web development (front-end and back-end)
- **C#** – Windows applications, game development (Unity)
- **Go** – Cloud services, networking
- **Rust** – Systems programming, safety

#### 4. Data Structures & Algorithms
- **Arrays, Linked Lists, Stacks, Queues** – Linear structures
- **Trees (Binary, AVL, B-trees)** – Hierarchical data
- **Graphs** – Networks, shortest path algorithms
- **Hash Tables** – Efficient key-value storage
- **Sorting Algorithms** – Quick sort, merge sort, heap sort
- **Searching Algorithms** – Binary search, BFS, DFS

#### 5. Operating Systems
- **Process Management** – Scheduling, synchronization
- **Memory Management** – Paging, segmentation
- **File Systems** – Storage organization
- **Examples**: Windows, Linux, macOS, Android

#### 6. Computer Networks
- **OSI and TCP/IP Models** – Layers and protocols
- **HTTP/HTTPS** – Web communication
- **DNS** – Domain name resolution
- **Network Security** – Firewalls, encryption

#### 7. Artificial Intelligence & Machine Learning
- **Machine Learning** – Supervised, unsupervised, reinforcement
- **Deep Learning** – Neural networks, CNNs, RNNs
- **Natural Language Processing** – Text analysis, chatbots
- **Computer Vision** – Image recognition, object detection

#### 8. Cybersecurity
- **Encryption** – Symmetric (AES), asymmetric (RSA)
- **Network Security** – Firewalls, intrusion detection
- **Ethical Hacking** – Penetration testing, vulnerability assessment

#### 9. Career Opportunities
- **Software Engineer/Developer**
- **Data Scientist / Machine Learning Engineer**
- **Cybersecurity Analyst**
- **Cloud Architect**
- **DevOps Engineer**
- **AI Research Scientist**
- **Game Developer**
- **Mobile App Developer**

#### 10. Future Scope
Computer Science continues to evolve with emerging fields like quantum computing, blockchain, IoT, and edge computing. The demand for skilled CS professionals remains high globally, with opportunities in tech giants, startups, research, and academia.
"""

    elif "artificial intelligence" in topic or "ai" in topic:
        return """
### Artificial Intelligence (AI) – In Depth

#### 1. Definition
Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (acquiring information and rules for using it), reasoning (using rules to reach conclusions), and self-correction.

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
"""

    elif "machine learning" in topic or "ml" in topic:
        return """
### Machine Learning (ML) – Detailed

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
- k-Nearest Neighbors (k-NN)
- K-Means Clustering
- Neural Networks

#### 4. Applications
- Spam filtering
- Image recognition
- Stock market prediction
- Customer segmentation
- Recommendation engines

#### 5. Tools & Libraries
- Python: scikit-learn, TensorFlow, PyTorch, Keras
- R: caret, randomForest
- Big data: Apache Spark MLlib
"""

    elif "cybersecurity" in topic or "cyber security" in topic:
        return """
### Cybersecurity – In Depth

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
- Man-in-the-Middle attacks
- Denial of Service (DoS)
- SQL Injection
- Zero-day exploits

#### 4. Security Measures
- Firewalls, Intrusion Detection Systems (IDS)
- Encryption (AES, RSA)
- Multi-factor Authentication (MFA)
- Regular patching and updates
- Security awareness training

#### 5. Career Paths
- Security Analyst
- Penetration Tester
- Security Engineer
- Chief Information Security Officer (CISO)
- Forensic Analyst
"""

    elif "cloud computing" in topic:
        return """
### Cloud Computing – Detailed

#### 1. Definition
Cloud computing is the on-demand delivery of IT resources over the internet with pay-as-you-go pricing. Instead of buying, owning, and maintaining physical data centers, you can access technology services, such as computing power, storage, and databases, from a cloud provider.

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
"""

    elif "software engineering" in topic:
        return """
### Software Engineering – In Depth

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
- **Agile** – Iterative development with cross-functional teams.
- **Scrum** – Agile framework with sprints.
- **Kanban** – Visual workflow management.
- **DevOps** – Integrating development and operations.

#### 4. Key Concepts
- **Object-Oriented Programming** – Encapsulation, inheritance, polymorphism.
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
"""
    
    else:
        return None

# -------------------- Knowledge Base (500+ Topics) --------------------
def load_knowledge_base():
    kb = []
    
    # Helper to add entries
    def add_entry(keywords, answer):
        kb.append({"keywords": keywords, "answer": answer})
    
    # ========== MAJOR TOPICS (detailed answers) ==========
    add_entry(["bca", "bachelor of computer applications", "tell me about bca", "explain bca", "bca course"], "DETAILED_BCA")
    add_entry(["computer science", "cs", "tell me about computer science", "explain computer science"], "DETAILED_CS")
    add_entry(["artificial intelligence", "ai", "what is ai", "explain ai"], "DETAILED_AI")
    add_entry(["machine learning", "ml", "what is machine learning", "explain ml"], "DETAILED_ML")
    add_entry(["cybersecurity", "cyber security", "what is cybersecurity"], "DETAILED_CYBERSECURITY")
    add_entry(["cloud computing", "what is cloud computing"], "DETAILED_CLOUD")
    add_entry(["software engineering", "what is software engineering"], "DETAILED_SOFTWARE_ENG")
    
    # ========== BCA SUBTOPICS (expanded) ==========
    add_entry(["bca subjects", "bca syllabus", "bca curriculum"],
              "BCA subjects include: Programming languages (C, C++, Java, Python), Data Structures, Database Management, Computer Networks, Operating Systems, Software Engineering, Web Development, Mathematics, and Cloud Computing basics. The syllabus is spread over 6 semesters, with each semester covering 5-6 subjects.")
    add_entry(["bca eligibility", "eligibility for bca"],
              "Eligibility for BCA: Candidates must have completed 10+2 (or equivalent) from a recognized board with Mathematics or Computer Science as a subject. Minimum aggregate marks typically range from 45% to 50% (relaxation for reserved categories). Some universities also require English as a subject.")
    add_entry(["bca duration", "bca course duration"],
              "BCA is a 3-year undergraduate program divided into 6 semesters. Some institutes offer part-time or distance learning options, but the standard duration is 3 years.")
    add_entry(["bca programming languages", "languages in bca"],
              "In BCA, students typically learn: C, C++, Java, Python, JavaScript, and sometimes PHP, SQL, and HTML/CSS. These languages cover procedural, object-oriented, and web development paradigms.")
    add_entry(["bca skills", "skills learned in bca"],
              "Skills developed during BCA: programming proficiency, problem-solving, database management, understanding of networking, software development lifecycle, teamwork, and project management. Students also gain analytical and communication skills.")
    add_entry(["jobs after bca", "career after bca", "bca job opportunities", "bca career paths"],
              "After BCA, common job roles include: Software Developer, Web Developer, Data Analyst, System Administrator, Network Engineer, Cybersecurity Analyst, Mobile App Developer, Cloud Engineer, DevOps Engineer, and Technical Support. Many graduates also pursue higher studies like MCA or MBA.")
    add_entry(["bca salary", "bca average salary", "bca salary in india"],
              "Average salary for BCA freshers in India ranges from ₹2.5 to 5 LPA. With experience and certifications, it can go up to ₹10-15 LPA or more. Salaries vary based on skills, company, and location.")
    add_entry(["bca future scope", "scope after bca", "future after bca"],
              "Future scope after BCA is bright. Graduates can work in IT companies, startups, government organizations, or as freelancers. With additional certifications in AI, data science, cloud, or cybersecurity, they can advance to specialized roles. Higher studies like MCA open doors to research and academia.")
    add_entry(["higher studies after bca", "mca after bca", "mba after bca", "mba it after bca"],
              "Popular higher studies after BCA: MCA (Master of Computer Applications) – 2 years, deepens computer knowledge; MBA in IT – management roles; MSc in Computer Science; Data Science or AI certifications; Cloud certifications (AWS, Azure).")
    add_entry(["bca vs cs", "bca vs computer science", "bca vs bsc cs"],
              "BCA is a professional undergraduate degree focused on applications and software development, while Computer Science is an academic discipline covering theory, algorithms, and systems. BCA is more industry-oriented; CS is broader and often pursued as B.Sc. CS or B.E./B.Tech. Both lead to careers in IT.")
    add_entry(["bca freelancing", "freelancing after bca"],
              "BCA graduates can freelance in web development, mobile app development, software testing, technical writing, and digital marketing. Platforms like Upwork, Fiverr, and Freelancer offer opportunities. Building a strong portfolio is key.")
    add_entry(["bca startup", "startup opportunities after bca"],
              "With programming and business skills, BCA graduates can launch startups in software development, e-commerce, ed-tech, or IT services. Incubators and government schemes like Startup India provide support.")
    add_entry(["bca industry demand", "demand for bca graduates"],
              "Demand for BCA graduates is high in IT companies, banks, government sectors, and multinational corporations. Roles in software development, data analytics, and cloud computing are particularly in demand.")
    add_entry(["bca projects", "projects for bca", "bca final year project"],
              "BCA projects help apply theoretical knowledge. Ideas: Library Management System, Online Quiz Portal, E-commerce Website, Chatbot, Weather App, Student Database, Hospital Management System. Use languages like Java, Python, PHP, and databases like MySQL.")
    add_entry(["bca internships", "internships for bca students"],
              "BCA students can intern as software developers, web developers, data analysts, or IT support. Internships provide industry exposure and improve employability. Platforms like Internshala, LinkedIn, and company career pages list opportunities.")
    
    # ========== COMPUTER SCIENCE GENERAL ==========
    add_entry(["history of computers", "computer history", "evolution of computers"],
              "The history of computers dates back to the abacus and mechanical calculators. Key milestones: Charles Babbage's Analytical Engine (1837), ENIAC (1945) – first electronic general-purpose computer, invention of transistors (1947), integrated circuits (1958), microprocessors (1971), personal computers (1980s), internet (1990s), and the era of AI and cloud computing today.")
    add_entry(["what is computer science", "cs definition", "define computer science"],
              "Computer Science is the study of computers and computational systems. It involves theory, design, development, and application of software and hardware. Key areas include algorithms, programming, data structures, artificial intelligence, and more.")
    add_entry(["computer science career", "cs career opportunities", "careers in computer science"],
              "Computer Science careers include: Software Engineer, Data Scientist, AI/ML Engineer, Cybersecurity Analyst, Cloud Architect, DevOps Engineer, Game Developer, Mobile App Developer, IT Consultant, and Research Scientist. Opportunities exist in tech companies, finance, healthcare, and government.")
    add_entry(["computer science future scope", "future of cs", "scope of computer science"],
              "The future of Computer Science is promising with emerging fields like quantum computing, edge computing, AI ethics, blockchain, IoT, and bioinformatics. CS professionals will continue to be in high demand as technology integrates into every aspect of life.")
    
    # ========== PROGRAMMING LANGUAGES (detailed) ==========
    languages = [
        ("python", "Python is a high-level, interpreted language known for simplicity and readability. It's widely used in web development (Django, Flask), data science (pandas, NumPy), AI/ML (TensorFlow, PyTorch), and automation. It has a large standard library and strong community support."),
        ("java", "Java is an object-oriented, platform-independent language. It's used for enterprise applications, Android development, and large-scale systems. Key features: JVM, garbage collection, strong typing, multithreading."),
        ("c++", "C++ is an extension of C with object-oriented features. It's used in game development, system software, embedded systems, and performance-critical applications. It provides low-level memory manipulation and high performance."),
        ("javascript", "JavaScript is the language of the web. It enables interactive web pages and is used on both client-side and server-side (Node.js). Frameworks: React, Angular, Vue. It's event-driven and supports asynchronous programming."),
        ("c#", "C# (C-Sharp) is a modern object-oriented language from Microsoft. It's used for Windows applications, game development with Unity, and enterprise software. It has features like LINQ, async/await, and strong typing."),
        ("php", "PHP is a server-side scripting language designed for web development. It powers many content management systems like WordPress, Joomla, and Drupal. It's easy to learn and integrates with databases."),
        ("swift", "Swift is Apple's language for iOS and macOS development. It's fast, safe, and expressive, replacing Objective-C. It supports protocol-oriented programming and has modern syntax."),
        ("kotlin", "Kotlin is a modern JVM language that interoperates with Java. It's officially supported for Android development and is concise and safe. It reduces boilerplate code and avoids null pointer exceptions."),
        ("ruby", "Ruby is a dynamic, object-oriented language known for its elegant syntax. It's popular with the Ruby on Rails framework for web development. It emphasizes convention over configuration."),
        ("go", "Go (Golang) is a compiled language by Google, designed for concurrency and simplicity. It's used in cloud services, networking, and DevOps tools. It has goroutines for lightweight concurrency."),
        ("rust", "Rust is a systems language focused on safety and performance. It's used for building reliable software, including operating systems and game engines. It guarantees memory safety without garbage collection."),
        ("typescript", "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. It adds static typing and modern features for large-scale applications. It improves developer productivity and code maintainability."),
        ("c language", "C is a procedural programming language developed by Dennis Ritchie. It's used for system programming, embedded systems, and operating systems. It provides low-level access to memory and is highly efficient."),
        ("sql", "SQL (Structured Query Language) is used to manage relational databases. It allows querying, inserting, updating, and deleting data. Key commands: SELECT, INSERT, UPDATE, DELETE, JOIN, CREATE TABLE."),
        ("r", "R is a programming language and environment for statistical computing and graphics. It's widely used among statisticians and data miners for developing statistical software and data analysis."),
        ("perl", "Perl is a high-level, interpreted language known for its text processing capabilities. It's used in system administration, web development, and network programming."),
        ("scala", "Scala is a language that combines object-oriented and functional programming. It runs on the JVM and is used for building scalable applications, especially with Apache Spark."),
        ("dart", "Dart is a client-optimized language for fast apps on any platform. It is used with the Flutter framework for building natively compiled applications for mobile, web, and desktop."),
        ("html", "HTML (HyperText Markup Language) is the standard markup language for creating web pages. It structures content with elements like headings, paragraphs, links, images, forms."),
        ("css", "CSS (Cascading Style Sheets) styles HTML elements. It controls layout, colors, fonts, and responsive design. Frameworks: Bootstrap, Tailwind. Preprocessors: Sass, Less."),
        ("bash", "Bash is a Unix shell and command language. It's used for scripting and automating tasks in Linux/Unix environments."),
        ("powershell", "PowerShell is a task automation and configuration management framework from Microsoft, consisting of a command-line shell and scripting language."),
    ]
    for lang, desc in languages:
        add_entry([lang, f"{lang} language", f"what is {lang}", f"explain {lang}", f"tell me about {lang}", f"learn {lang}"], desc)
    
    # ========== DATA STRUCTURES ==========
    ds = [
        ("data structures", "Data structures are ways to organize and store data efficiently. Common ones: arrays, linked lists, stacks, queues, trees, graphs, hash tables. Choosing the right data structure is crucial for algorithm performance."),
        ("array", "An array is a collection of elements stored at contiguous memory locations. It allows random access via index. Used for storing lists of data. Time complexity: access O(1), search O(n), insertion/deletion O(n)."),
        ("linked list", "A linked list is a linear data structure where elements (nodes) are linked using pointers. Types: singly, doubly, circular. It allows efficient insertion/deletion O(1) at known position but slow access O(n)."),
        ("stack", "A stack is a LIFO (Last In First Out) data structure. Operations: push (add), pop (remove), peek (top). Used in function calls, expression evaluation, undo operations, and backtracking."),
        ("queue", "A queue is a FIFO (First In First Out) data structure. Operations: enqueue (add), dequeue (remove). Used in scheduling, breadth-first search, and task management. Variants: circular queue, priority queue, deque."),
        ("tree", "A tree is a hierarchical data structure with nodes connected by edges. Binary trees, binary search trees, AVL trees, B-trees, heaps are common. Used in file systems, databases (indexing), HTML DOM, and decision trees."),
        ("binary tree", "A binary tree is a tree where each node has at most two children. Types: full, complete, perfect, balanced. Traversals: inorder, preorder, postorder, level-order."),
        ("binary search tree", "A binary search tree (BST) is a binary tree where left child < parent < right child. It allows efficient search, insertion, deletion O(log n) on average. Balanced BSTs (AVL, Red-Black) maintain O(log n) worst-case."),
        ("graph", "A graph consists of vertices and edges. It can be directed or undirected, weighted or unweighted. Used in social networks, maps, recommendation systems. Algorithms: BFS, DFS, Dijkstra, A*, Bellman-Ford, Floyd-Warshall."),
        ("hash table", "A hash table (or hash map) stores key-value pairs. It uses a hash function to compute an index. Provides O(1) average lookup, insertion, deletion. Used in databases, caches, dictionaries. Collision resolution: chaining, open addressing."),
        ("heap", "A heap is a specialized tree-based data structure that satisfies the heap property. Max-heap: parent >= children; Min-heap: parent <= children. Used in priority queues, heap sort."),
        ("trie", "A trie is a tree-like data structure for storing strings. Each node represents a common prefix. Used in autocomplete, spell checkers, IP routing."),
    ]
    for topic, desc in ds:
        add_entry([topic, f"what is {topic}", f"explain {topic}", f"tell me about {topic}"], desc)
    
    # ========== ALGORITHMS ==========
    algos = [
        ("algorithms", "Algorithms are step-by-step procedures for solving problems. Key concepts: sorting (quick sort, merge sort), searching (binary search), recursion, dynamic programming, and complexity analysis (Big O notation)."),
        ("sorting algorithms", "Sorting arranges data in order. Common algorithms: Bubble Sort (simple but slow), Quick Sort (fast average), Merge Sort (stable, O(n log n)), Heap Sort (in-place), Insertion Sort (good for small data). Time complexities vary."),
        ("quick sort", "Quick sort is a divide-and-conquer algorithm. It picks a pivot and partitions the array around it. Average time O(n log n), worst-case O(n²) but can be avoided with good pivot selection. In-place but not stable."),
        ("merge sort", "Merge sort is a divide-and-conquer algorithm that divides the array into halves, sorts them, and merges. Time O(n log n) always, stable, but requires O(n) extra space."),
        ("binary search", "Binary search finds the position of a target value in a sorted array. It compares the target to the middle element and eliminates half. Time O(log n). Requires sorted data."),
        ("dynamic programming", "Dynamic programming solves complex problems by breaking them into simpler subproblems and storing results to avoid recomputation. Used in optimization problems like Fibonacci, knapsack, shortest path."),
        ("recursion", "Recursion is a technique where a function calls itself to solve smaller instances. It requires a base case and recursive case. Used in tree traversals, divide-and-conquer algorithms."),
        ("big o notation", "Big O notation describes the upper bound of an algorithm's time or space complexity. Examples: O(1) constant, O(log n) logarithmic, O(n) linear, O(n²) quadratic, O(2^n) exponential."),
        ("greedy algorithm", "Greedy algorithms make the locally optimal choice at each stage, hoping to find a global optimum. Examples: Huffman coding, Dijkstra's algorithm, activity selection."),
        ("backtracking", "Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally and removing solutions that fail constraints. Examples: N-Queens, Sudoku, maze solving."),
        ("divide and conquer", "Divide and conquer algorithms work by recursively breaking down a problem into subproblems, solving them, and combining results. Examples: merge sort, quick sort, binary search."),
    ]
    for topic, desc in algos:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== OPERATING SYSTEMS ==========
    os_topics = [
        ("operating system", "An operating system (OS) manages computer hardware and software. Examples: Windows, macOS, Linux, Android. Key functions: process management, memory management, file systems, device management, security."),
        ("process management", "Process management involves creating, scheduling, and terminating processes. Concepts: PCB, states (new, ready, running, waiting, terminated), context switching, IPC (pipes, message queues, shared memory)."),
        ("cpu scheduling", "CPU scheduling decides which process gets the CPU. Algorithms: FCFS, SJF, Round Robin, Priority. Goals: maximize throughput, minimize response time, avoid starvation."),
        ("memory management", "Memory management allocates and deallocates memory. Techniques: paging, segmentation, virtual memory, demand paging. Concepts: logical vs physical address, MMU, page faults, thrashing."),
        ("file system", "A file system controls how data is stored and retrieved. Examples: NTFS, FAT32, ext4, APFS. It organizes files into directories, manages metadata, and ensures data integrity."),
        ("linux", "Linux is an open-source OS kernel. Distributions: Ubuntu, Fedora, CentOS, Debian. Widely used in servers, development, and embedded systems. It follows Unix philosophy and supports multitasking, multiuser."),
        ("windows", "Windows is a popular OS from Microsoft with a graphical interface. Versions: Windows 10, 11, Server. It supports a wide range of software and hardware, with features like task manager, registry, and PowerShell."),
        ("macos", "macOS is Apple's OS for Mac computers. Known for its Unix-based architecture and seamless integration with Apple devices. It has a sleek UI and is popular among developers and creatives."),
        ("android", "Android is a mobile operating system based on Linux. It's developed by Google and used in smartphones, tablets, and smart devices. It has a large app ecosystem and customizable interface."),
        ("ios", "iOS is Apple's mobile operating system for iPhones and iPads. Known for its security, smooth performance, and integration with Apple services."),
        ("deadlock", "Deadlock is a situation where two or more processes are unable to proceed because each is waiting for resources held by the other. Conditions: mutual exclusion, hold and wait, no preemption, circular wait. Solutions: prevention, avoidance, detection, recovery."),
    ]
    for topic, desc in os_topics:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== COMPUTER NETWORKS ==========
    net = [
        ("computer networks", "Computer networks connect multiple devices to share resources and data. Types: LAN, WAN, MAN. Key concepts: IP addresses, protocols, OSI model, TCP/IP, routing, switching."),
        ("osi model", "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application. It standardizes network communication and helps in troubleshooting."),
        ("tcp/ip", "TCP/IP is the fundamental protocol suite for the internet. TCP ensures reliable delivery, IP handles addressing and routing. It has 4 layers: Application, Transport, Internet, Network Access."),
        ("http", "HTTP (Hypertext Transfer Protocol) is used for web communication. HTTPS adds encryption. Methods: GET, POST, PUT, DELETE, PATCH. It is stateless and works over TCP."),
        ("dns", "DNS (Domain Name System) translates domain names (like google.com) into IP addresses. It is a hierarchical system with root servers, TLD servers, and authoritative name servers."),
        ("ip address", "An IP address is a unique identifier for a device on a network. IPv4 uses 32-bit addresses (e.g., 192.168.1.1), IPv6 uses 128-bit. It can be static or dynamic."),
        ("firewall", "A firewall monitors and controls incoming/outgoing network traffic based on security rules. It acts as a barrier between trusted and untrusted networks. Types: packet-filtering, stateful, application-layer."),
        ("router", "A router forwards data packets between computer networks. It uses routing tables and protocols (RIP, OSPF, BGP) to determine the best path."),
        ("switch", "A switch connects devices on a local area network (LAN) and uses MAC addresses to forward data to the correct destination."),
        ("vpn", "VPN (Virtual Private Network) extends a private network across a public network, enabling users to send and receive data as if their devices were directly connected to the private network. It provides privacy and security."),
        ("ethernet", "Ethernet is a family of wired networking technologies commonly used in LANs. It defines physical and data link layer specifications."),
        ("wifi", "Wi-Fi is a wireless networking technology that uses radio waves to provide high-speed internet and network connections."),
    ]
    for topic, desc in net:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== DATABASE MANAGEMENT ==========
    db = [
        ("database management", "Database management involves storing, organizing, and retrieving data. DBMS (Database Management System) software like MySQL, Oracle, SQL Server. It ensures data integrity, security, and concurrency."),
        ("sql", "SQL (Structured Query Language) is used to manage relational databases. Commands: SELECT, INSERT, UPDATE, DELETE, JOIN, CREATE TABLE, ALTER, DROP. It also includes subqueries, views, and transactions."),
        ("nosql", "NoSQL databases are non-relational and handle unstructured data. Types: document (MongoDB), key-value (Redis), column-family (Cassandra), graph (Neo4j). They are scalable and flexible for big data."),
        ("acid", "ACID properties ensure reliable database transactions: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions don't interfere), Durability (committed changes persist)."),
        ("normalization", "Normalization organizes data to reduce redundancy and improve integrity. Normal forms: 1NF (atomic values), 2NF (remove partial dependencies), 3NF (remove transitive dependencies), BCNF (stronger)."),
        ("mysql", "MySQL is an open-source relational database management system. It uses SQL and is widely used for web applications (LAMP stack). It supports ACID transactions, stored procedures, triggers."),
        ("mongodb", "MongoDB is a NoSQL document database. It stores data in JSON-like documents with dynamic schemas. It is scalable, high-performance, and used for modern applications."),
        ("postgresql", "PostgreSQL is a powerful, open-source object-relational database system. It supports advanced data types, full-text search, and extensibility."),
        ("oracle", "Oracle Database is a multi-model database management system commonly used for enterprise applications. It offers robust features, scalability, and security."),
        ("redis", "Redis is an in-memory data structure store, used as a database, cache, and message broker. It supports data structures like strings, hashes, lists, sets."),
        ("cassandra", "Apache Cassandra is a distributed NoSQL database designed for handling large amounts of data across many commodity servers, providing high availability with no single point of failure."),
        ("neo4j", "Neo4j is a graph database that stores data in nodes and relationships. It's used for applications like social networks, recommendation engines, and fraud detection."),
    ]
    for topic, desc in db:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== ARTIFICIAL INTELLIGENCE & MACHINE LEARNING ==========
    ai_ml = [
        ("artificial intelligence", "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes learning, reasoning, perception, and problem-solving. Subfields: ML, NLP, computer vision, robotics."),
        ("machine learning", "Machine Learning (ML) is a subset of AI where systems learn from data. Types: supervised (labeled data), unsupervised (unlabeled), reinforcement (reward-based). Algorithms: linear regression, decision trees, SVM, neural networks."),
        ("deep learning", "Deep Learning uses neural networks with many layers. It powers image recognition, speech recognition, and natural language processing. Frameworks: TensorFlow, PyTorch, Keras."),
        ("neural networks", "Neural networks are computing systems inspired by biological brains. They consist of layers of interconnected nodes (neurons). Used in deep learning for complex pattern recognition. Types: CNN, RNN, GAN."),
        ("natural language processing", "NLP enables computers to understand and generate human language. Applications: chatbots, translation, sentiment analysis. Techniques: tokenization, word embeddings (Word2Vec, BERT), transformers."),
        ("computer vision", "Computer vision enables machines to interpret visual data. Used in facial recognition, object detection, medical imaging. Libraries: OpenCV, YOLO, TensorFlow Object Detection."),
        ("ai vs machine learning", "AI is the broad field of creating intelligent machines, while ML is a subset of AI that enables machines to learn from data without explicit programming. Deep learning is a further subset of ML using neural networks."),
        ("supervised learning", "Supervised learning uses labeled data to train models. Examples: classification (spam detection), regression (price prediction). Algorithms: linear regression, logistic regression, SVM, random forest."),
        ("unsupervised learning", "Unsupervised learning finds patterns in unlabeled data. Examples: clustering (customer segmentation), association (market basket analysis). Algorithms: K-means, hierarchical clustering, Apriori."),
        ("reinforcement learning", "Reinforcement learning involves an agent learning by interacting with an environment, receiving rewards or penalties. Used in game playing, robotics, self-driving cars."),
        ("nlp", "Natural Language Processing (NLP) is a field of AI that gives machines the ability to read, understand, and derive meaning from human languages."),
        ("chatbot", "A chatbot is a software application used to conduct an on-line chat conversation via text or text-to-speech, in lieu of providing direct contact with a live human agent."),
    ]
    for topic, desc in ai_ml:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== CYBERSECURITY ==========
    cyber = [
        ("cybersecurity", "Cybersecurity protects systems, networks, and data from digital attacks. Key areas: network security, application security, information security, incident response, disaster recovery."),
        ("encryption", "Encryption converts data into a coded form to prevent unauthorized access. Symmetric (AES, DES) uses same key; asymmetric (RSA, ECC) uses public/private keys. Used in HTTPS, secure messaging, file encryption."),
        ("ethical hacking", "Ethical hacking (penetration testing) simulates attacks to identify vulnerabilities. Ethical hackers use tools like Metasploit, Nmap, Wireshark to test systems and report findings."),
        ("malware", "Malware (malicious software) includes viruses, worms, trojans, ransomware, spyware, adware. It can steal data, damage systems, or encrypt files. Protection: antivirus, firewalls, safe browsing."),
        ("phishing", "Phishing is a social engineering attack where attackers impersonate legitimate entities to trick users into revealing sensitive information. Awareness and email filters help prevent."),
        ("cybersecurity career", "Cybersecurity careers include: Security Analyst, Penetration Tester, Security Engineer, CISO, Incident Responder. Skills needed: networking, operating systems, scripting, risk assessment. Certifications: CEH, CISSP, CompTIA Security+."),
        ("ransomware", "Ransomware is a type of malware that encrypts the victim's files and demands a ransom for decryption. Prevention: regular backups, security updates, user training."),
        ("firewall", "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies."),
        ("ids", "Intrusion Detection System (IDS) monitors network traffic for suspicious activity and alerts administrators. Types: network-based (NIDS), host-based (HIDS)."),
        ("ips", "Intrusion Prevention System (IPS) is similar to IDS but also takes action to block or prevent detected threats."),
    ]
    for topic, desc in cyber:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== CLOUD COMPUTING ==========
    cloud = [
        ("cloud computing", "Cloud computing delivers computing services over the internet. Models: IaaS (Infrastructure), PaaS (Platform), SaaS (Software). Providers: AWS, Azure, Google Cloud. Benefits: scalability, cost-efficiency, reliability."),
        ("aws", "Amazon Web Services (AWS) is a comprehensive cloud platform offering compute (EC2), storage (S3), databases (RDS), and more. It has global infrastructure and pay-as-you-go pricing."),
        ("azure", "Microsoft Azure is a cloud platform with services for computing, analytics, storage, and networking. Integrates well with Microsoft products. Supports hybrid cloud and AI services."),
        ("google cloud", "Google Cloud Platform (GCP) offers cloud services including Compute Engine, App Engine, BigQuery, and Kubernetes. It is strong in data analytics and machine learning."),
        ("docker", "Docker is a platform for developing, shipping, and running applications in containers. Containers are lightweight, portable, and consistent across environments. Docker images are built from Dockerfiles."),
        ("kubernetes", "Kubernetes (K8s) is an open-source system for automating deployment, scaling, and management of containerized applications. It groups containers into pods and manages clusters."),
        ("cloud engineer career", "Cloud engineers design, deploy, and manage cloud infrastructure. Skills: cloud platforms (AWS, Azure), automation (Terraform, Ansible), containerization (Docker, Kubernetes). Certifications: AWS Solutions Architect, Azure Administrator."),
        ("iaas", "Infrastructure as a Service (IaaS) provides virtualized computing resources over the internet. Users can rent virtual machines, storage, and networks. Examples: AWS EC2, Google Compute Engine."),
        ("paas", "Platform as a Service (PaaS) provides a platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining infrastructure. Examples: Heroku, Google App Engine."),
        ("saas", "Software as a Service (SaaS) delivers software applications over the internet on a subscription basis. Examples: Google Workspace, Salesforce, Microsoft 365."),
        ("serverless", "Serverless computing allows developers to build and run applications without managing servers. The cloud provider dynamically manages the allocation of resources. Examples: AWS Lambda, Azure Functions."),
    ]
    for topic, desc in cloud:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== SOFTWARE ENGINEERING ==========
    se = [
        ("software engineering", "Software engineering applies engineering principles to software development. It includes requirements analysis, design, implementation, testing, and maintenance. Methodologies: Agile, Waterfall, DevOps."),
        ("software development life cycle", "SDLC is a process for planning, creating, testing, and deploying software. Phases: Requirement Analysis, Design, Implementation, Testing, Deployment, Maintenance. Models: Waterfall, Agile, Spiral, V-model."),
        ("agile", "Agile is an iterative approach to software development that emphasizes flexibility, collaboration, and customer feedback. Scrum and Kanban are popular Agile frameworks. It delivers working software in short sprints."),
        ("scrum", "Scrum is an Agile framework with roles (Product Owner, Scrum Master, Development Team), events (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Increment)."),
        ("devops", "DevOps is a culture and set of practices that combine development (Dev) and IT operations (Ops). It aims to shorten the development lifecycle and provide continuous delivery. Tools: Jenkins, Git, Docker, Kubernetes."),
        ("version control", "Version control systems track changes to code over time. Git is the most popular, with platforms like GitHub, GitLab. Commands: init, add, commit, push, pull, branch, merge."),
        ("testing", "Software testing ensures quality. Types: unit testing (individual components), integration testing (combined modules), system testing (whole system), acceptance testing (user requirements). Automated testing tools: JUnit, Selenium, pytest."),
        ("object oriented programming", "OOP is a programming paradigm based on objects containing data and methods. Key concepts: encapsulation, inheritance, polymorphism, abstraction. Languages: Java, C++, Python, C#."),
        ("oop concepts", "Four main OOP concepts: Encapsulation (bundling data and methods), Inheritance (creating new classes from existing ones), Polymorphism (same interface for different data types), Abstraction (hiding complexity)."),
        ("system design", "System design involves defining architecture, components, modules, and data to satisfy requirements. It includes high-level design (HLD) and low-level design (LLD). Key considerations: scalability, reliability, performance."),
        ("apis", "API (Application Programming Interface) allows software applications to communicate. REST, GraphQL, SOAP are common. APIs expose endpoints with methods (GET, POST) and return data (JSON, XML)."),
        ("git", "Git is a distributed version control system. Commands: clone, add, commit, push, pull, branch, merge. Platforms: GitHub, GitLab, Bitbucket. It enables collaboration and code history tracking."),
        ("jenkins", "Jenkins is an open-source automation server used for continuous integration and continuous delivery (CI/CD). It helps automate building, testing, and deploying software."),
        ("jira", "Jira is a project management tool used for issue tracking and agile project management. It's popular among software development teams."),
    ]
    for topic, desc in se:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== WEB DEVELOPMENT ==========
    web = [
        ("web development", "Web development involves building websites and web applications. Front-end (client-side) and back-end (server-side). Technologies: HTML, CSS, JavaScript, frameworks, databases, APIs."),
        ("html", "HTML (HyperText Markup Language) is the standard markup language for creating web pages. It structures content with elements like headings, paragraphs, links, images, forms."),
        ("css", "CSS (Cascading Style Sheets) styles HTML elements. It controls layout, colors, fonts, and responsive design. Frameworks: Bootstrap, Tailwind. Preprocessors: Sass, Less."),
        ("javascript", "JavaScript is the programming language of the web. It adds interactivity to web pages. It runs in browsers and on servers (Node.js). Libraries: jQuery, React, Angular, Vue."),
        ("frontend development", "Front-end development focuses on the user interface. Languages: HTML, CSS, JavaScript. Frameworks: React, Angular, Vue. Tools: npm, webpack, Babel."),
        ("backend development", "Back-end development handles server-side logic, databases, and APIs. Languages: Python (Django, Flask), JavaScript (Node.js), Java (Spring), PHP (Laravel), Ruby (Rails). It manages authentication, data processing."),
        ("full stack development", "Full stack development involves both front-end and back-end. A full stack developer can build entire web applications. Popular stacks: MERN (MongoDB, Express, React, Node), MEAN (MongoDB, Express, Angular, Node), LAMP (Linux, Apache, MySQL, PHP)."),
        ("responsive design", "Responsive design ensures websites look good on all devices (desktop, tablet, mobile). Techniques: fluid grids, flexible images, media queries. Frameworks like Bootstrap make it easier."),
        ("react", "React is a JavaScript library for building user interfaces. Developed by Facebook, it allows building reusable UI components and efficiently updating the DOM."),
        ("angular", "Angular is a TypeScript-based web application framework developed by Google. It provides a comprehensive solution for building client-side applications."),
        ("vue", "Vue.js is a progressive JavaScript framework for building user interfaces. It is designed to be incrementally adoptable and focuses on the view layer."),
        ("nodejs", "Node.js is a JavaScript runtime built on Chrome's V8 engine. It allows running JavaScript on the server-side, enabling full-stack JavaScript development."),
        ("django", "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It includes an ORM, admin interface, and authentication."),
        ("flask", "Flask is a lightweight WSGI web application framework in Python. It is designed to be simple and extensible."),
        ("spring", "Spring is a powerful Java framework for building enterprise applications. It provides comprehensive infrastructure support for developing Java applications."),
    ]
    for topic, desc in web:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    # ========== CAREER PATHS (SPECIFIC) ==========
    careers = [
        ("software developer career", "Software developers design, code, and test software. Skills: programming languages (Java, Python, C#), problem-solving, teamwork. Path: learn languages, build projects, contribute to open source, prepare for interviews. Certifications: Oracle Certified Professional, AWS Developer."),
        ("data science career", "Data scientists analyze data to extract insights. Skills: Python, R, SQL, statistics, machine learning. Path: learn tools (pandas, scikit-learn), work on projects, get certifications (IBM Data Science, Google Data Analytics). Roles: Data Analyst, Data Engineer, ML Engineer."),
        ("ai engineer career", "AI engineers build AI models and systems. Skills: machine learning, deep learning, Python, TensorFlow, PyTorch. Path: master math/statistics, take online courses, contribute to AI projects. Certifications: TensorFlow Developer Certificate, AWS AI."),
        ("cybersecurity career", "Cybersecurity professionals protect systems. Roles: Security Analyst, Penetration Tester, Security Architect. Skills: networking, OS, scripting, risk assessment. Certifications: CEH, CISSP, CompTIA Security+."),
        ("cloud engineer career", "Cloud engineers manage cloud infrastructure. Skills: AWS/Azure/GCP, automation (Terraform), containerization (Docker, Kubernetes). Path: get cloud certifications, build projects. Certifications: AWS Solutions Architect, Azure Administrator."),
        ("how to become a software developer", "1. Choose a programming language (Python, Java). 2. Learn fundamentals (data structures, algorithms). 3. Build projects (web apps, tools). 4. Contribute to open source. 5. Prepare for interviews (LeetCode). 6. Apply for internships/jobs. Continuous learning is key."),
        ("devops career", "DevOps engineers bridge development and operations. Skills: scripting (Python, Bash), CI/CD tools, containerization, cloud platforms. Certifications: AWS DevOps Engineer, Docker Certified Associate."),
        ("web developer career", "Web developers build websites and web apps. Front-end: HTML, CSS, JavaScript. Back-end: Node.js, Python, PHP. Full-stack: both. Build a portfolio, learn frameworks, and stay updated."),
    ]
    for topic, desc in careers:
        add_entry([topic, topic.replace("career", "career path"), f"how to become a {topic.split()[0]}"], desc)
    
    # ========== ADDITIONAL TOPICS (to exceed 600) ==========
    extra = [
        ("blockchain", "Blockchain is a decentralized, distributed ledger technology. It records transactions across many computers so that the record cannot be altered retroactively. Used in cryptocurrencies (Bitcoin), smart contracts, supply chain, voting."),
        ("iot", "Internet of Things (IoT) connects physical devices to the internet. Applications: smart homes, wearables, industrial automation, healthcare monitoring. Devices collect and exchange data using sensors and connectivity."),
        ("big data", "Big data refers to extremely large datasets that require specialized tools. Technologies: Hadoop, Spark, Kafka. Characteristics: volume, velocity, variety. Used in analytics, machine learning, business intelligence."),
        ("data science", "Data science combines statistics, programming, and domain knowledge to extract insights from data. It involves data cleaning, exploration, modeling, and visualization. Tools: Python (pandas, NumPy, scikit-learn), R, SQL."),
        ("quantum computing", "Quantum computing uses quantum bits (qubits) to perform computations. It leverages superposition and entanglement to solve problems faster than classical computers. Potential applications: cryptography, optimization, drug discovery."),
        ("compiler design", "Compiler design involves translating high-level language to machine code. Phases: lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, code generation. Tools: Lex, Yacc."),
        ("distributed systems", "Distributed systems consist of multiple computers that appear as a single coherent system. They communicate over a network and coordinate via protocols. Examples: cloud computing, peer-to-peer networks, distributed databases."),
        ("computer architecture", "Computer architecture describes the design of computer systems. It includes CPU design, instruction set architecture, memory hierarchy, I/O. Concepts: pipelining, caching, parallelism."),
        ("human computer interaction", "HCI studies how people interact with computers. It focuses on usability, user experience, interface design. Principles: visibility, feedback, consistency, affordance."),
        ("software testing", "Software testing verifies that software meets requirements and finds defects. Types: manual, automated, black-box, white-box, performance, security. Tools: Selenium, JUnit, TestNG."),
        ("rest api", "REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP methods (GET, POST, PUT, DELETE) and are stateless."),
        ("graphql", "GraphQL is a query language for APIs that allows clients to request exactly the data they need. It provides a more efficient and flexible alternative to REST."),
        ("microservices", "Microservices architecture structures an application as a collection of small, loosely coupled services. Each service is independently deployable and scalable."),
        ("serverless", "Serverless computing allows developers to run code without provisioning servers. The cloud provider manages the infrastructure. Examples: AWS Lambda, Azure Functions."),
        ("ci/cd", "CI/CD (Continuous Integration/Continuous Delivery) is a practice that automates the integration and delivery of code changes. Tools: Jenkins, GitLab CI, CircleCI."),
        ("terraform", "Terraform is an infrastructure as code tool that allows you to define and provision infrastructure using a declarative configuration language."),
        ("ansible", "Ansible is an open-source automation tool for configuration management, application deployment, and task automation. It uses YAML playbooks."),
        ("prometheus", "Prometheus is an open-source monitoring and alerting toolkit commonly used in cloud-native environments."),
        ("grafana", "Grafana is an open-source analytics and visualization platform that integrates with various data sources."),
        ("elasticsearch", "Elasticsearch is a distributed search and analytics engine based on Lucene. It's used for log analytics, full-text search, and more."),
        ("kafka", "Apache Kafka is a distributed event streaming platform used for building real-time data pipelines and streaming applications."),
        ("spark", "Apache Spark is a unified analytics engine for large-scale data processing. It supports SQL, streaming, machine learning, and graph processing."),
        ("hadoop", "Apache Hadoop is a framework for distributed storage and processing of big data using the MapReduce programming model."),
        ("flink", "Apache Flink is a stream processing framework for real-time data processing."),
    ]
    for topic, desc in extra:
        add_entry([topic, f"what is {topic}", f"explain {topic}"], desc)
    
    return kb

KNOWLEDGE_BASE = load_knowledge_base()

# -------------------- Helper Functions --------------------
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def get_bot_response(user_input):
    try:
        normalized = normalize_text(user_input)
        
        # First check knowledge base with word-boundary matching to avoid false positives
        for item in KNOWLEDGE_BASE:
            for keyword in item["keywords"]:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, normalized):
                    if item["answer"].startswith("DETAILED_"):
                        # Map to detailed answer function
                        topic_map = {
                            "DETAILED_BCA": "bca",
                            "DETAILED_CS": "computer science",
                            "DETAILED_AI": "artificial intelligence",
                            "DETAILED_ML": "machine learning",
                            "DETAILED_CYBERSECURITY": "cybersecurity",
                            "DETAILED_CLOUD": "cloud computing",
                            "DETAILED_SOFTWARE_ENG": "software engineering"
                        }
                        return get_detailed_answer(topic_map.get(item["answer"], ""))
                    return item["answer"]
        
        # If no match, check for major topics via detailed answer directly
        detailed = get_detailed_answer(user_input)
        if detailed:
            return detailed
        
        return "Sorry, I am designed to answer questions related to Computer Science and BCA only."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# -------------------- Session State --------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your CS/BCA assistant. Ask me about programming, algorithms, career paths, or any computer science topic."}
    ]

# -------------------- Custom CSS (Modern, Animated, Poppins, Glassmorphism) --------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
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
        background-size: 300% 300%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
            
    @keyframes floatOrbs {
        0% { transform: translate(0, 0) scale(1); opacity: 0.5; }
        33% { transform: translate(2%, 3%) scale(1.05); opacity: 0.7; }
        66% { transform: translate(-1%, 2%) scale(0.98); opacity: 0.6; }
        100% { transform: translate(0, 0) scale(1); opacity: 0.5; }
    }

    /* Glassmorphism base */
    .glass {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }

    /* Fade-in animation for elements */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeInUp 1s ease forwards;
    }

    /* Typewriter effect for subtitle */
    .typewriter {
        display: inline-block;
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid rgba(255,255,255,0.7);
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }
    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: rgba(255,255,255,0.7); }
    }

    /* Hero card */
    .hero-card {
            max-width: 900px;
        width: 90%;
        margin: 2rem auto;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 60px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 30px 60px rgba(0,0,0,0.4);
        text-align: center;
        transition: all 0.4s;
        animation: fadeInUp 1.2s ease;
        position: relative;
        z-index: 2;
        box-sizing: border-box;
    }

    .hero-card:hover {
        transform: translateY(-8px);
        border-color: rgba(255,255,255,0.5);
        box-shadow: 0 40px 80px rgba(0,0,0,0.5);
    }

    /* Icon with glowing pulse */
    .icon-container {
        position: relative;
        width: 140px;
        height: 140px;
        margin: 0 auto 1.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .robot-icon {
        font-size: 5.8rem;
        position: relative;
        z-index: 2;
    }
    .glow-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 120px;
        height: 120px;
        background: radial-gradient(circle,
            rgba(102,126,234,1) 0%,
            rgba(102,126,234,0.7) 40%,
            rgba(102,126,234,0.2) 65%,
            rgba(102,126,234,0) 80%);
        border-radius: 50%;
        animation: pulseGlow 3s ease-out infinite;
        z-index: 1;
    }
    @keyframes pulseGlow {
        0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.8; }
        50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.4; }
        100% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.8; }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    @keyframes neonGlow {
        from {
            text-shadow:
                0 0 5px #667eea,
                0 0 10px #667eea,
                0 0 20px #667eea,
                0 0 40px #764ba2;
        }
        to {
            text-shadow:
                0 0 10px #667eea,
                0 0 20px #667eea,
                0 0 40px #764ba2,
                0 0 80px #764ba2;
        }
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
        text-align: center;

        text-shadow:
            0 0 5px #667eea,
            0 0 10px #667eea,
            0 0 20px #667eea,
            0 0 40px #764ba2,
            0 0 80px #764ba2;

        animation: neonGlow 2s ease-in-out infinite alternate;
    }
    .hero-subtitle{
        font-size: 1.45rem;
        font-weight: 500;
        color: #ffffff;
        text-align: center;

        margin: 0.6rem auto 1rem auto;
        max-width: 80%;        /* line card ke andar rahegi */
        line-height: 1.6;

        white-space: normal;   /* wrap allow */
        overflow-wrap: break-word;
        word-break: break-word;
        
        border-right: none;
        animation: none;
    }
    .hero-credit {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 1rem;

        text-shadow:
            0 0 5px rgba(102,126,234,0.6),
            0 0 10px rgba(102,126,234,0.6);
    }
    .hero-meta {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 500;

        text-shadow:
            0 0 4px rgba(118,75,162,0.6),
            0 0 8px rgba(118,75,162,0.6);
    }

    /* Stats row */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        margin: 2rem 0 3rem;
        flex-wrap: wrap;
        z-index: 2;
        position: relative;
    }
    .stat-card {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 1.8rem 3rem;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        transition: all 0.3s;
        animation: fadeInUp 1.4s ease;
        min-width: 180px;
    }
    .stat-card:hover {
        transform: scale(1.05);
        border-color: rgba(255,255,255,0.5);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        line-height: 1.2;
        text-shadow: 0 0 15px rgba(255,255,255,0.3);
    }
    .stat-label {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.8);
    }

    /* Section titles */
    .section-title {
        text-align: center;
        color: white;
        font-size: 2.8rem;
        font-weight: 600;
        margin: 3rem 0 2rem;
        text-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease;
    }

    /* Feature cards grid */
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 3rem;
        max-width: 1300px;
        margin: 3.5rem auto;
        padding: 1rem 2rem;
        justify-items: center;
        position: relative;
        z-index: 2;
    }
    .feature-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius: 35px;
        padding: 2.5rem;
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.4s;
        animation: fadeInUp 1.5s ease;
        text-align: center;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255,255,255,0.4);
        box-shadow: 0 30px 50px rgba(0,0,0,0.4);
    }
    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 1.2rem;
    }
    .card-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1rem;
    }
    .card-desc {
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        line-height: 1.5;
    }
    .topic-list {
        margin-top: 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }
    .topic-tag {
        background: rgba(255,255,255,0.15);
        border-radius: 40px;
        padding: 0.3rem 1rem;
        font-size: 0.8rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Popular topics chips */
    .chips-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        max-width: 1000px;
        margin: 2rem auto;
        position: relative;
        z-index: 2;
    }
    .chip-btn {
        background: rgba(255,255,255,0.12);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 0.8rem 1.8rem;
        border-radius: 50px;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
        border: none;
        font-weight: 500;
    }
    .chip-btn:hover {
        background: rgba(255,255,255,0.25);
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* Launch button */
    .launch-btn-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0 3rem;
        position: relative;
        z-index: 2;
    }
    .launch-btn {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        padding: 1.2rem 4rem;
        border: none;
        border-radius: 70px;
        cursor: pointer;
        transition: all 0.4s;
        box-shadow: 0 15px 35px rgba(102,126,234,0.5);
        border: 1px solid rgba(255,255,255,0.2);
        display: inline-block;
        text-align: center;
        animation: pulse 3s infinite;
    }
    .launch-btn:hover {
        transform: scale(1.08);
        box-shadow: 0 25px 50px rgba(102,126,234,0.7);
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102,126,234,0.7); }
        70% { box-shadow: 0 0 0 15px rgba(102,126,234,0); }
        100% { box-shadow: 0 0 0 0 rgba(102,126,234,0); }
    }

    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.6);
        padding: 2rem;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }

    /* Navigation bar for chat page */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        position: relative;
        z-index: 10;
    }
    .nav-btn {
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 0.7rem 1.8rem;
        border-radius: 40px;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 1rem;
        font-weight: 500;
    }
    .nav-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Chat header */
    .chat-header {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border-radius: 50px;
        padding: 2rem;
        margin: 1rem auto 2rem;
        max-width: 800px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        animation: fadeInUp 0.8s ease;
    }
    .chat-header h1 {
        color: white;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .chat-header p {
        color: rgba(255,255,255,0.8);
        font-size: 1.2rem;
    }

    /* Message bubbles */
    .message-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .message {
        display: flex;
        margin-bottom: 1.5rem;
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
        padding: 1.2rem 2rem;
        border-radius: 30px;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        word-wrap: break-word;
        font-size: 1rem;
        line-height: 1.5;
    }
    .message.user .message-bubble {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-bottom-right-radius: 8px;
    }
    .message.assistant .message-bubble {
        background: rgba(255,255,255,0.2);
        border-bottom-left-radius: 8px;
    }

    /* Suggestion buttons */
    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        justify-content: center;
        max-width: 800px;
        margin: 1rem auto;
    }
    .suggestion-btn {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 40px;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
    }
    .suggestion-btn:hover {
        background: rgba(255,255,255,0.25);
        transform: scale(1.02);
        border-color: rgba(255,255,255,0.4);
    }

    /* Chat input */
    .stChatInput {
        max-width: 700px;
        margin: 0 auto !important;
    }
    .stChatInput > div {
        border-radius: 60px !important;
        background: rgba(255,255,255,0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        transition: all 0.3s !important;
        padding: 0.7rem 1.5rem !important;
    }
    .stChatInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102,126,234,0.3) !important;
    }
    .stChatInput input {
        color: white !important;
        font-size: 1rem !important;
    }
    .stChatInput input::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }

    /* Override Streamlit buttons */
    div.stButton > button {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        border-radius: 40px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: none !important;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.3) !important;
        transform: scale(1.02) !important;
        border-color: rgba(255,255,255,0.5) !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------- Navigation Functions --------------------
def go_to_chat():
    st.session_state.page = "chat"

def go_to_landing():
    st.session_state.page = "landing"

# -------------------- Landing Page --------------------
def render_landing():
    # Hero Card
    st.markdown("""
    <div class="hero-card fade-in">
        <div class="icon-container">
            <div class="glow-circle"></div>
            <div class="robot-icon">🤖</div>
        </div>
        <div class="hero-title">Secure AI Agent</div>
        <div class="hero-subtitle typewriter">Smart, Secure & Real-Time AI Assistant — Built for intelligent and safe human interaction.</div>
        <div class="hero-credit">Created by Mirza Jaffar Ali Baig | Aims Degree College</div>
        <div class="hero-meta">Built using Python & Streamlit | Open Source Project</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats Row
    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-number">600+</div>
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

    # Feature Cards Section
    st.markdown("<h2 class='section-title'>What I Can Help You With</h2>", unsafe_allow_html=True)

    # Define cards with topics
    cards = [
        ("💻", "Computer Science", "Algorithms, data structures, programming languages, OS, networks, and more.",
         ["Algorithms", "Data Structures", "Programming", "OS", "Networks"]),
        ("📚", "BCA & Academics", "Course structure, syllabus, subjects, and academic guidance for BCA.",
         ["BCA Syllabus", "Subjects", "Projects", "Internships"]),
        ("🚀", "Career Guidance", "Jobs after BCA, software dev paths, data science, cybersecurity careers.",
         ["Software Developer", "Data Scientist", "AI Engineer", "Cloud Architect"]),
        ("🤖", "AI & Machine Learning", "Neural networks, deep learning, NLP, computer vision, and AI ethics.",
         ["Neural Networks", "Deep Learning", "NLP", "Computer Vision"]),
        ("☁️", "Cloud & DevOps", "AWS, Azure, Docker, Kubernetes, CI/CD, and infrastructure as code.",
         ["AWS", "Docker", "Kubernetes", "CI/CD"]),
        ("🔒", "Cybersecurity", "Encryption, network security, ethical hacking, risk management.",
         ["Encryption", "Firewalls", "Pen Testing", "Malware"]),
    ]

    # Display cards in grid (2 rows, 3 columns)
    st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(cards):
                icon, title, desc, topics = cards[i+j]
                with col:
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

    # Popular Topics Chips
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
    # Create clickable chips that navigate to chat and send the question
    st.markdown("<div class='chips-container'>", unsafe_allow_html=True)
    for q in popular_questions:
        if st.button(q, key=f"chip_{q}"):
            st.session_state.pending_question = q
            go_to_chat()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Launch Button (big)
    st.markdown("<div class='launch-btn-container'>", unsafe_allow_html=True)
    if st.button("🚀 Launch Secure AI", key="launch_big"):
        go_to_chat()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        © 2026 Secure AI Agent — CS/BCA Academic Assistant. All rights reserved.
    </div>
    """, unsafe_allow_html=True)

# -------------------- Chat Page --------------------
def render_chat():
    # Navigation bar
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        if st.button("🏠 Home", key="home"):
            go_to_landing()
            st.rerun()
    with col3:
        if st.button("🧹 Clear Chat", key="clear"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your CS/BCA assistant. Ask me about programming, algorithms, career paths, or any computer science topic."}
            ]
            st.rerun()

    # Chat Header
    st.markdown("""
    <div class="chat-header">
        <h1>💬 CS/BCA Assistant</h1>
        <p>Ask me anything about Computer Science or BCA</p>
    </div>
    """, unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message user">
                <div class="message-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant">
                <div class="message-bubble">{msg["content"]}</div>
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
            response = get_bot_response(s)
            with st.spinner("Typing..."):
                time.sleep(1.2)  # simulate typing
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Handle pending question from landing page chips
    if "pending_question" in st.session_state:
        q = st.session_state.pending_question
        del st.session_state.pending_question
        st.session_state.messages.append({"role": "user", "content": q})
        response = get_bot_response(q)
        with st.spinner("Typing..."):
            time.sleep(1.2)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Chat input
    prompt = st.chat_input("Type your question here...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = get_bot_response(prompt)
        with st.spinner("Typing..."):
            time.sleep(1.2)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# -------------------- Main --------------------
if st.session_state.page == "landing":
    render_landing()
else:
    render_chat()