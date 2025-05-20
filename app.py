from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import process  # Import fuzzywuzzy's process module

# Initialize the Flask app
app = Flask(__name__)

# Knowledge base with keywords and corresponding responses
knowledge_base = {
    "heyy": "Yess how can I assist you",
    "hello": "Yess how can I assist you",
    "ask":"yeahh i will answer what I know",
    "college name":"Maharaja Institute Of Technology Mysore",
    "mit":"Maharaja Institute Of Technology Mysore",
    "who are you": "I am VaNaM a newly introduced chatbot at Maharaja Institute Of Technology Mysore assisting queries",
    "your name": "I am VaNaM a newly introduced chatbot at Maharaja Institute Of Technology Mysore assisting queries",
    "How are you": "I am fine How can I assist you..",
    "VaNaM": "VaNaM its a ChatBot Name 1) Va is taken from the name of Dr Vasudev T Secretary,MET and Dean,ISE 2) Na is taken from the name of Dr Naresh Kumar B G Principal,MiT Mysore 3) M is taken from Murali S President,MET  ",
    "about your college": "MITM is situated at a beautiful, enchanting and sprawling landscape about 3 kms behind K.R.Mills. The institute is founded by a group of eminent people recognised for their eminence in the field of science and engineering technology. Many of them have served at the highest levels of AICTE and University.The college is equipped with all modern learning aids to make teaching-learning process a pleasure. The highly qualified staff is its asset.The college has to its credit the highest number of admissions in the academic year 2007-08 among the 16 newly opened engineering colleges in Karnataka.",
    "your college": "MITM is situated at a beautiful, enchanting and sprawling landscape about 3 kms behind K.R.Mills. The institute is founded by a group of eminent people recognised for their eminence in the field of science and engineering technology. Many of them have served at the highest levels of AICTE and University.The college is equipped with all modern learning aids to make teaching-learning process a pleasure. The highly qualified staff is its asset.The college has to its credit the highest number of admissions in the academic year 2007-08 among the 16 newly opened engineering colleges in Karnataka.",
    "about MIT college": "MITM is situated at a beautiful, enchanting and sprawling landscape about 3 kms behind K.R.Mills. The institute is founded by a group of eminent people recognised for their eminence in the field of science and engineering technology. Many of them have served at the highest levels of AICTE and University.The college is equipped with all modern learning aids to make teaching-learning process a pleasure. The highly qualified staff is its asset.The college has to its credit the highest number of admissions in the academic year 2007-08 among the 16 newly opened engineering colleges in Karnataka.",
    "courses": "We offer undergraduate and postgraduate courses in Engineering, Business. Would you like to know about a specific graduation level specify(UG/PG)",
    "Engineering": "At the undergraduate level, it provides Bachelor of Engineering(B.E) degrees in fields such as Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Civil Engineering, Mechanical Engineering, Information Science and Engineering (ISE), Computer Science & Engineering(Artificial Intelligence and Machine Learning (AI & ML)), and Computer Science & Engineering ( Artificial Intelligence ),Computer Science & Engineering ( Data Science ),Computer science & Business System,Computer Engineering ,Computer Science & Engineering(IOT & Cyber Security including Block Chain Technology )",
    "branches":"At the undergraduate level, it provides Bachelor of Engineering(B.E) degrees in fields such as Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Civil Engineering, Mechanical Engineering, Information Science and Engineering (ISE), Computer Science & Engineering(Artificial Intelligence and Machine Learning (AI & ML)), and Computer Science & Engineering ( Artificial Intelligence ),Computer Science & Engineering ( Data Science ),Computer science & Business System,Computer Engineering ,Computer Science & Engineering(IOT & Cyber Security including Block Chain Technology )",
    "streams": "Maharaja Institute of Technology (MIT) Mysore offers a wide range of undergraduate and postgraduate programs across various disciplines. At the undergraduate level, it provides Bachelor of Engineering (B.Es) degrees in fields such as Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Electrical and Electronics Engineering (EEE), Civil Engineering, Mechanical Engineering, Information Science and Engineering (ISE), Artificial Intelligence and Data Science (AI & DS), and Automobile Engineering. For postgraduate students, MIT Mysore offers Master of Technology (M.Tech) degrees in specializations like Computer Science, Structural Engineering, Digital Electronics and Communication, VLSI Design and Embedded Systems, and Power Electronics. Additionally, the institute offers MBA (Master of Business Administration) and MCA (Master of Computer Applications) programs, catering to students interested in management and computer science. These diverse streams provide ample opportunities for students to pursue careers in engineering, technology, and management.",
    "admission": "We provide admissions for all the degrees based on Counselling(CET/COMED-K) Or Management quota. Specify the quota (CET/COMED-K/MANAGEMENT) to get details about admissions or For more information Call: 9620228022 or Visit our Admission page https://mitmysore.in/general-info/ ",
    "PG":"At the postgraduate level, we provide Master of Buisness Administration,Master of Computer Applications,M.Tech in Thermal engineering,M.Tech in CSE,M.Tech in LSP",
    "under graduate":"At the undergraduate level, it provides Bachelor of Engineering(B.E) degrees in fields such as Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Civil Engineering, Mechanical Engineering, Information Science and Engineering (ISE), Computer Science & Engineering(Artificial Intelligence and Machine Learning (AI & ML)), and Computer Science & Engineering ( Artificial Intelligence ),Computer Science & Engineering ( Data Science ),Computer science & Business System,Computer Engineering ,Computer Science & Engineering(IOT & Cyber Security including Block Chain Technology )",
    "UG":"At the undergraduate level, it provides Bachelor of Engineering(B.E) degrees in fields such as Computer Science and Engineering (CSE), Electronics and Communication Engineering (ECE), Civil Engineering, Mechanical Engineering, Information Science and Engineering (ISE), Computer Science & Engineering(Artificial Intelligence and Machine Learning (AI & ML)), and Computer Science & Engineering ( Artificial Intelligence ),Computer Science & Engineering ( Data Science ),Computer science & Business System,Computer Engineering ,Computer Science & Engineering(IOT & Cyber Security including Block Chain Technology )",
    "CET":"KEA seats will be allotted to consoled college.Students will download the Admission Order.Students must submit the allotment letter with relevant documents to the accounts section.Account personnel must check the allotment letter of the students and issue the MIT Mysore admission application form by receiving Application fees.",
    "COMEDK":"COMEDK seat will be allotted to consoled college.Students will download the Admission Order.Students must submit the allotment letter with relevant documents to the accounts section.Account personnel must check the allotment letter of the students and issue the MIT Mysore admission application form by receiving Application fees.",
    "management":"The aspiring candidates will meet the Principal seeking admission to MIT Mysore.After the discussion/counseling of the candidate and his/her parents/guardians by the Principal, the candidate will be permitted to take the MIT Mysore application form from the accounts section.On approval of the Principal, the account section must issue the MIT Mysore admission application form by receiving Application fees.",
    "fees": "The fees structure varies depending on the course, but it ranges from 100000 to 200000 per year.And we accept online payments to proceed use https://eazypay.icicibank.com/eazypayLink?P1=600dLcy/1FTRKUhrPTAJyg==",
    "fees structure for engineering":"Sorry I can't provide fees structure for specific courses accurately you visit our Admission Office for more details",
    "post graduate":"At the postgraduate level, we provide Master of Buisness Administration,Master of Computer Applications,M.Tech in Thermal engineering,M.Tech in CSE,M.Tech in LSP",
    "hostel": "Yes, we have both boys' and girls' hostels on campus.",
    "location": "Our college is situated at Belavadi Village, Srirangapatna Taluk, Mandya District about 3 km from Columbia Asia Hospital Junction Mysore at beautiful, enchanting and sprawling landscape",
    "located": "Our college is situated at Belavadi Village, Srirangapatna Taluk, Mandya District about 3 km from Columbia Asia Hospital Junction Mysore at beautiful, enchanting and sprawling landscape",
    "situated": "Our college is situated at Belavadi Village, Srirangapatna Taluk, Mandya District about 3 km from Columbia Asia Hospital Junction Mysore at beautiful, enchanting and sprawling landscape",
    "extracurricular": "We offer a variety of extracurricular activities including sports, music, drama, and more.",
    "scholarship": "We are not providing any scholarship instead we provide fees concession for the academic toppers",
    "timings":"Monday to saturday : 9:00 - 4:00 & Sunday : Closed",
    "president":"Dr Murali S is the president of Maharaja Education Trust Mysore",
    "secretary":"Dr. Thimmaiah Vasudev is the secretary of Maharaja Education Trust & Dean of the Department Of ISE",
    "owner":"Ooops its confidential",
    "ok bye": "Bye",
    "thank you": "Yeahh have a nice day",
    "sports":"Physical Education Department Physical education is an integral part of young people’s education. In this course, students can learn about the importance of being physically active as part of a healthy lifestyle. Physical Education Department has an important contribution to make in supporting students to discover ways in which they can increase their enjoyment, confidence and competence in a range of physical activities.",
    "hi": "Hello",
    "placement":"We provide best placement oportunities and click on 'PLACEMENT' at 'Quick Link' to get more details about placements",
    "college autonomous":"Yess our college is autonomus institution affiliated to Visveswaraya Technological University Belagavi from the academic year 2023-24",
    "trust":"Maharaja Education Trust® was established in the year 2005 not just as a venture but to serve the society with the educational institutions driven by the motive to provide well balanced learning environment in educating young minds. The Trust is governed by the board comprising of reputable and well-accomplished academicians learnt in premier institutes of the nation who have served at the highest possible roles in the broad education spectrum of the country.",
    "MET":"Maharaja Education Trust® was established in the year 2005 not just as a venture but to serve the society with the educational institutions driven by the motive to provide well balanced learning environment in educating young minds. The Trust is governed by the board comprising of reputable and well-accomplished academicians learnt in premier institutes of the nation who have served at the highest possible roles in the broad education spectrum of the country.",
    "maharaja education trust":"Maharaja Education Trust® was established in the year 2005 not just as a venture but to serve the society with the educational institutions driven by the motive to provide well balanced learning environment in educating young minds. The Trust is governed by the board comprising of reputable and well-accomplished academicians learnt in premier institutes of the nation who have served at the highest possible roles in the broad education spectrum of the country.",
    "cet codes":"E158CV(Civil Engineering) ,E158CS(Computer Science & Engineering) ,E158CI(Computer Science & Engineering ( Artificial Intelligence )) ,E158CD(Computer Science & Engineering ( Data Science )) ,E158CB(Computer science & Business System) ,E158EC(Electronics & Communication  Engineering) ,E158IS(Information Science & Engineering), E158ME(Mechanical Engineering) ,E158MK(Mechanical Engineering ( Kannada Medium )), E158CE(Computer Engineering), E158CA(Computer Science & Engineering(Artificial Intelligence & Machine Learning )), E158IC(Computer Science & Engineering(IOT & Cyber Security including Block Chain Technology )) ",
    "gallery":"Sorry I can assist you with queries and i cant provide you images as response.Please click on'GALLERY' at'Quick Links' to view ",
    "images":"Sorry I can assist you with queries and i cant provide you images as response.Please click on'GALLERY' at'Quick Links' to view",
    "photos":"Sorry I can assist you with queries and i cant provide you images as response.Please click on'GALLERY' at'Quick Links' to view",
    "vision":"To be recognized as a premier technical and management institution promoting extensive education fostering research, innovation and entrepreneurial attitude",
    "mission":"To empower students with indispensable knowledge through dedicated teaching and collaborative learning.To advance extensive research in science, engineering and management disciplines.To facilitate entrepreneurial skills through effective institute-industry collaboration and interaction with alumni.To instill the need to uphold ethics in every aspect.To mould holistic individuals capable of contributing to the advancement of the society.",
    "vission and mission":"Vision is To be recognized as a premier technical and management institution promoting extensive education fostering research, innovation and entrepreneurial attitude and Mission is To empower students with indispensable knowledge through dedicated teaching and collaborative learning.To advance extensive research in science, engineering and management disciplines.To facilitate entrepreneurial skills through effective institute-industry collaboration and interaction with alumni.To instill the need to uphold ethics in every aspect.To mould holistic individuals capable of contributing to the advancement of the society.",
    "principal":"Dr. B G Naresh Kumar, is an academician and an administrator, maintained the spirit of teaching since 38 years, molding many civil engineers.His career as a teacher, administrator, structural engineer, researcher and mentor to many students is highly appreciated and acknowledged by many beneficiaries.",
    "notes":"Sure here is the link https://mitmysore.in/digital-notes/ or click on 'E-NOTES' at 'Quick Links'",
    "civil":"Dr. C Ramakrishnegowda Professor and Head, Department of Civil Engineering",
    "cv":"Dr. C Ramakrishnegowda Professor and Head, Department of Civil Engineering ",
    "cse":"Dr. Shivamurthy  R C	Professor and Head, Dept. of Computer Science and Engineering",
    "cs":"Dr. Shivamurthy  R C	Professor and Head, Dept. of Computer Science and Engineering",
    "computer science":"Dr. Shivamurthy  R C	Professor and Head, Dept. of Computer Science and Engineering",
    "ise":"Dr. Sharath Kumar Y H	Professor and Head, Department of Information and Science and Engineering",
    "IS":"Dr. Sharath Kumar Y H	Professor and Head, Department of Information and Science and Engineering",
    "csbs":"Dr Honnaraju B Professor and Head, Department of Computer Science and Buisness Systems",
    "computer science and buisness system":"Dr Honnaraju B Professor and Head, Department of Computer Science and Buisness Systems",
    "csds":"Dr Pushpa D Professor and Head, Department of Computer Science and Enghineering(Data Science)",
    "data science":"Dr Pushpa D Professor and Head, Department of Computer Science and Enghineering(Data Science)",
    "information science":"Dr. Sharath Kumar Y H	Professor and Head, Department of Information and Science and Engineering",
    "mechanical":"Dr. Mohamed Khaisar	Professor and Head, Department of  Mechanical Engineering",
    "chemistry":"Dr. B Manju	Professor and Head, Dept. of Chemistry",
    "physics":"Dr. Vijaylakshmi Dayal	Professor and Head, Department of Physics",
    "maths":"Dr. A H Srinivas	Associate Professor and Head, Dept. of Mathematics",
    "mathematics":"Dr. A H Srinivas	Associate Professor and Head, Dept. of Mathematics",
    "mca":"Prof. Manjunath B	Assistant Professor and Head, Department of Master of Computer Applications",
    "mba":"Dr. Shyam B R	Associate Professor and Head, Department of Master of Business Administrators",
    "Administrative  Officer":"Prof Aniruddha A M is the AO and PRO of MiT Mysore",
    "AO":"Prof Aniruddha A M is the AO and PRO of MiT Mysore",
    "PRO":"Prof Aniruddha A M is the AO and PRO of MiT Mysore",
    "nss officer":"Mr. Kiran Kumar L is our NSS officer",
    "best":"Yes its best engineering college",
    "safe":"Yes its safest college ",
    "autonomous":"MiT Mysore is an autonomous institution affiliated to VTU Belagavi from the academic year 2023-24",
    "director":"its preserved",
    "employees":"237 and more each branch has teaching and non teaching staffs",
    "area":"MIT has campus area of 25 acres",
    "staffs":"237 and more each branch has teaching and non teaching staffs",
    "alumini":"8000 and more aluminis",
    "recruiters":"200 and more recruiters",
    "students":"4000 and more",
    "student":"4000 and more",
    "infrastructure":"MITM is situated at a beautiful, enchanting and sprawling landscape about 3 kms behind K.R.Mills. The institute is founded by a group of eminent people recognised for their eminence in the field of science and engineering technology. Many of them have served at the highest levels of AICTE and University.The college is equipped with all modern learning aids to make teaching-learning process a pleasure. The highly qualified staff is its asset.The college has to its credit the highest number of admissions in the academic year 2007-08 among the 16 newly opened engineering colleges in Karnataka.",
    "event":"Click on 'Events' at 'Quick Links'",
    "humanities":"Prof Uma Bhavani Professor and Head, Dept Of Humanities",
    "pet":"Dhanya sundar Professor and Head,Department Of Physical Education",
    "physical":"Dhanya sundar Professor and Head,Department Of Physical Education",
    "ec":"Dr Parimala R V Professor and Head, Department of Electronics and Communications",
    "ece":"Dr Parimala R V Professor and Head, Department of Electronics and Communications",
    "electronics and communications":"Dr Parimala R V Professr and Head, Department of Electronics and Communications",
    "coe":"Dr Sharath Kumar Y H is the working Controller Of Examination at MIT Mysore",
    "controller of examination":"Dr Sharath Kumar Y H is the working Controller Of Examination at MIT Mysore",
    "library":"Library uses Koha, Integrated Library Management Software, which supports in-house operations of library such as acquisition, cataloguing, circulation, serials control and OPAC. Database is up-to-date.Smart circulation system is used successfully via Bar-code technology for all the resources and barrower cards.For more details visit  https://mitlibraryblog.wordpress.com/e-journals/",
    "question bank":"Yeah sure click on 'QUESTION BANK' at 'Quick Links' and you can download it",
    "transportation":"Transportation and Parking Services offers the MIT community a single location for all transportation and parking information. Students, faculty, staff and visitors will find information on MIT College parking rules and regulations, inter-campus transportation, commuting aids, maps, directions and a host of links.Transportation and Parking Services coordinates and/or assists in the coordination of all transportation-related services and programs for special events, athletic events, handicapped access and parking, signage, way-finding, all rideshare activities and many other related services.You can get Bus route details here https://mitmysore.in/wp-content/uploads/2021/01/MITM_Bus-Route_Jan-2021.pdf ",
    "nss":"NSS and YRC Units are the social extension forums of MITM. These forums instill the great humanitarian spirit and values in the student community by making them participate in many kinds of social service activities. It makes the students socially responsible, caring and accountable citizens of the nation.",
    "cafeteria":"MIT Mysorem has good cafetria inside the campus and assuring quality food",
    "canteen":"MIT Mysorem has good cafetria inside the campus and assuring quality food",
    "kutira":"Ravi Kumar Kutira it is a garden located inside MiT Mysore Campus",
    "teachers":"MiT Mysore has well trained professor and HOD's with intutive knowledge",
     "lecturers":"MiT Mysore has well trained professor and HOD's with intutive knowledge",
     "professor":"MiT Mysore has well trained professor and HOD's with intutive knowledge",
    
    "examinations":"MiT Mysore is an autonomous institution affiliated to VTU Belagavi, the Examinations are controlled by Controller Of Examination in well mannered way",
   "exams":"MiT Mysore is an autonomous institution affiliated to VTU Belagavi, the Examinations are controlled by Controller Of Examination in well mannered way",
    "Dr. Naresh Kumar B G":"Principal of MIT Mysore"
}

# Function to find keywords and generate a response
def get_response(user_query):
    # Convert user query to lowercase for better matching
    user_query = user_query.lower()

    # Check if the user query exactly matches any keyword (ignoring case)
    for keyword in knowledge_base.keys():
        if user_query == keyword.lower():
            return knowledge_base[keyword]

    # If exact match isn't found, use fuzzywuzzy to find the best match
    best_match = process.extractOne(user_query, knowledge_base.keys())
    
    if best_match:
        matched_keyword, score = best_match
        # If the match is strong enough (e.g., 80% similarity), return the corresponding response
        if score >= 90:
            # Only suggest 'Did you mean' if the user query is not an exact match
            return f"\n{knowledge_base[matched_keyword]}"

    # If no keyword matches or the similarity is too low, return a default response
    return "Sorry, I'm still under development and learning, so I may not be able to answer all your questions. Try using other words or click on 'Official Website' at Quick Links"

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API route for chatbot response
@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_input = request.form['user_input']
    bot_response = get_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
