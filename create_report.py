from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'SkillLoop_Project_Report.pdf'
pdfmetrics.registerFont(TTFont('Tinos','/usr/share/fonts/truetype/croscore/Tinos-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-Bold','/usr/share/fonts/truetype/croscore/Tinos-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-Italic','/usr/share/fonts/truetype/croscore/Tinos-Italic.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle',parent=styles['Title'],fontName='Tinos-Bold',fontSize=27,leading=33,textColor=colors.HexColor('#282342'),alignment=TA_CENTER,spaceAfter=12))
styles.add(ParagraphStyle(name='CoverSub',parent=styles['Normal'],fontName='Tinos-Italic',fontSize=14,leading=20,textColor=colors.HexColor('#655A9B'),alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1x',parent=styles['Heading1'],fontName='Tinos-Bold',fontSize=18,leading=22,textColor=colors.HexColor('#302A50'),spaceAfter=10))
styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontName='Tinos-Bold',fontSize=13,leading=16,textColor=colors.HexColor('#51458D'),spaceBefore=7,spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontName='Tinos',fontSize=12,leading=16.5,spaceAfter=7,alignment=TA_LEFT))
styles.add(ParagraphStyle(name='Smallx',parent=styles['BodyText'],fontName='Tinos',fontSize=10,leading=13.5,spaceAfter=4))
styles.add(ParagraphStyle(name='CodeX',parent=styles['Code'],fontName='Courier',fontSize=8.5,leading=11,backColor=colors.HexColor('#F3F2F8'),borderPadding=8))
P=lambda t,style='Bodyx':Paragraph(t,styles[style])
story=[]

def page(title, kicker=None):
    if kicker: story.append(P(kicker.upper(),'Smallx'))
    story.append(P(title,'H1x'))

def bullets(items):
    for x in items: story.append(Paragraph('• '+x,styles['Bodyx']))

def table(data,widths=None):
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAE7F8')),('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#302A50')),('FONTNAME',(0,0),(-1,0),'Times-Bold'),('FONTNAME',(0,1),(-1,-1),'Times-Roman'),('FONTSIZE',(0,0),(-1,-1),9.5),('LEADING',(0,0),(-1,-1),12),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#D8D5E4')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(t);story.append(Spacer(1,8))

# 1 Cover
story += [Spacer(1,35*mm),P('SKILLLOOP','CoverTitle'),P('A Campus-Based Peer-to-Peer Skill Exchange Platform','CoverSub'),Spacer(1,12*mm),P('<b>Project Report</b>','H2x'),P('Submitted in partial fulfilment of the requirements for the course: <b>[COURSE / SUBJECT NAME]</b>'),Spacer(1,8*mm)]
table([['TEAM MEMBER','ROLL NUMBER'],['Aman','[ENTER ROLL NUMBER]'],['Iksha','[ENTER ROLL NUMBER]']],[80*mm,70*mm])
story += [Spacer(1,8*mm),P('<b>Department:</b> [DEPARTMENT NAME]'),P('<b>Institution:</b> [COLLEGE / UNIVERSITY NAME]'),P('<b>Faculty Guide:</b> [FACULTY NAME]'),P('<b>Academic Year:</b> 2026–27'),Spacer(1,20*mm),P('Submission date: [ENTER DATE]','CoverSub'),PageBreak()]

# 2 Abstract
page('Abstract and Introduction','01 — Project overview')
story.append(P('SkillLoop is a campus-oriented platform intended to help students exchange knowledge directly with one another. A student can list skills they are comfortable teaching, skills they want to learn, their availability, and their preferred learning mode. The platform identifies reciprocal learning opportunities and allows a student to send an exchange request.'))
story.append(P('The project is designed as an academic demonstration of object-oriented programming in C++. The domain model, student search, compatibility calculation, ranking, exchange workflow and CSV persistence are implemented in a C++17 engine. Streamlit provides a browser-based interface, while Python libraries support descriptive analytics.'))
story.append(P('The architecture deliberately separates presentation from business logic. Streamlit collects user input and displays results; it does not calculate matches. It invokes the C++ executable through a small Python adapter. This makes the C++ engine independently compilable and testable while keeping the demonstration accessible through a web browser.'))
story.append(P('The current recommendation method is deterministic and rule-based. It is not a machine-learning model and the project does not claim predictive AI.'))
story.append(P('Keywords: C++, object-oriented programming, Streamlit, reciprocal matching, CSV, data analytics.'))
story.append(PageBreak())

# 3 Problem/objectives
page('Problem Statement and Objectives','02 — Need and scope')
story.append(P('<b>Problem statement.</b> Students often possess useful skills but lack a structured way to discover classmates who can teach the skills they want to learn. Informal requests are difficult to coordinate, and a one-sided skill overlap does not guarantee a mutually beneficial exchange.'))
story.append(P('<b>Proposed solution.</b> SkillLoop maintains student skill profiles and searches for pairs where each student can teach at least one skill the other wants to learn. It ranks eligible pairs using availability and learning-mode compatibility, then records exchange requests.'))
story.append(P('<b>Objectives</b>'))
bullets(['Create and maintain student profiles with skills offered and skills wanted.','Identify reciprocal skill-exchange opportunities rather than one-sided overlaps.','Calculate an interpretable compatibility score and rank matches.','Create, accept and decline exchange requests.','Persist student and exchange records using portable CSV files.','Demonstrate major C++ OOP concepts in the actual business-logic implementation.','Analyse campus skill supply and demand using Python and visualisations.'])
story.append(P('<b>Scope.</b> The prototype focuses on a small campus community and a demonstrable workflow. Secure authentication, messaging, calendar synchronisation, large-scale concurrency and a production database are outside the current scope.'))
story.append(PageBreak())

# 4 Existing/proposed
page('Existing System and Proposed System','03 — System comparison')
story.append(P('<b>Existing approach.</b> Students typically rely on class groups, friends or informal social messages to find someone who can teach a skill. These methods are fragmented and do not systematically check whether both participants benefit.'))
story.append(P('<b>Proposed SkillLoop system.</b> Profiles represent teaching and learning preferences in a consistent structure. The C++ matching engine checks reciprocal compatibility, calculates a score and returns ranked candidates. An exchange request provides a simple workflow for recording the next step.'))
table([['Aspect','Informal approach','SkillLoop prototype'],['Discovery','Manual messages and word of mouth','Searchable student profiles and ranked matches'],['Compatibility','Usually judged informally','Reciprocal skill check plus weighted score'],['Request tracking','Scattered messages','Pending / Accepted / Declined status'],['Records','Unstructured','CSV records'],['Insights','No consolidated view','Supply, demand and skill-gap charts']],[35*mm,58*mm,65*mm])
story.append(P('<b>Expected benefits.</b> More discoverable peer learning opportunities, clearer expectations, a traceable request status, and a simple overview of which skills are commonly offered or requested.'))
story.append(PageBreak())

# 5 requirements
page('Requirements and Technology Stack','04 — Requirements')
story.append(P('<b>Functional requirements</b>'))
bullets(['Select a demo student identity and view the community dashboard.','Create and update a student profile.','Store teaching skills, learning goals, availability and mode.','Generate reciprocal matches and show compatibility scores.','Send exchange requests and allow the recipient to accept or decline.','Display skill supply, demand and demand-gap analytics.'])
story.append(P('<b>Non-functional requirements</b>'))
bullets(['Maintain a clear separation between interface and business logic.','Use portable, human-readable CSV storage for the prototype.','Provide understandable error messages when the C++ compiler or data files are unavailable.','Keep the interface responsive and readable in a desktop browser.','Make the core engine independently compilable and testable.'])
table([['Technology','Role'],['C++17 / g++','OOP domain model, matching, search and exchange operations'],['Streamlit','Browser interface and user interaction'],['Python subprocess adapter','Calls the compiled C++ engine'],['Pandas / Matplotlib','Descriptive analysis and charts'],['CSV','Student and exchange persistence']],[45*mm,113*mm])
story.append(PageBreak())

# 6 architecture
page('System Architecture and Data Flow','05 — Design')
story.append(P('The design uses a layered architecture. The Streamlit presentation layer communicates with a Python adapter. The adapter compiles the C++ source when required and invokes the engine with structured command-line arguments. C++ reads or updates CSV files and returns tab-separated results for the interface to render.'))
story.append(P('STREAMLIT PRESENTATION  →  PYTHON ADAPTER  →  C++17 ENGINE  →  CSV STORAGE','CodeX'))
story.append(P('The analytics module independently reads the student CSV file with Pandas. It counts the number of students offering and seeking each skill, calculates a demand gap, and generates charts.'))
story.append(P('<b>Reason for this design.</b> The C++ engine remains the source of truth for matching and exchange operations. Streamlit keeps the application easy to open through a browser and avoids requiring Qt or a JavaScript frontend. A command-line boundary also allows the C++ engine to be tested without the UI.'))
story.append(P('<b>Deployment note.</b> The repository includes a Streamlit Community Cloud configuration with `packages.txt` requesting g++. The hosting environment must support installing the compiler and building the C++ executable at startup. A deployed URL must be generated and verified from the team’s own hosting account.'))
story.append(PageBreak())

# 7 class design
page('Class Design and Relationships','06 — C++ OOP design')
table([['Class','Responsibility / relationship'],['User','Abstract base class; private identity data; pure virtual role and dashboardMessage methods'],['Student','Publicly inherits User; stores course, year, skills, availability and mode'],['Admin','Publicly inherits User; overrides role-specific virtual behaviour'],['Match','Encapsulates candidate details and compatibility score; overloads operator>'],['DataManager','Loads and writes Student and Exchange records in CSV files'],['StudentService','Implements overloaded searchStudents methods'],['MatchEngine','Checks reciprocal skill fit, scores and ranks candidates'],['ExchangeService','Creates exchange requests through DataManager']],[35*mm,123*mm])
story.append(P('<b>Inheritance.</b> Student and Admin are specialised forms of User. Shared identity information and the common interface are defined once in the base class.'))
story.append(P('<b>Association and composition.</b> MatchEngine operates on Student objects supplied by the application. DataManager is used by services to persist domain records. The classes are separated by responsibility rather than putting every operation into one large class.'))
story.append(PageBreak())

# 8 OOP
page('Implementation of Major OOP Concepts','07 — Academic mapping')
table([['OOP concept','Where demonstrated'],['Encapsulation','Private fields in User and Match; public getters and controlled setters'],['Abstraction','User is abstract and declares pure virtual role-specific methods'],['Inheritance','Student and Admin derive from User'],['Runtime polymorphism','Virtual methods are called through User smart pointers in user_demo'],['Constructors / destructors','Constructors initialise objects; virtual User destructor supports safe base-pointer destruction'],['Function overloading','StudentService::searchStudents(name), searchStudents(name, course), searchStudents(name, year)'],['Operator overloading','Match::operator> compares compatibility scores; ranking uses it'],['Dynamic memory','std::make_unique creates polymorphic objects with automatic lifetime management']],[39*mm,119*mm])
story.append(P('The implementation uses RAII and `std::unique_ptr` rather than manually managing raw pointers. This still demonstrates dynamic allocation while reducing memory-leak risk. The virtual destructor ensures correct destruction through a base-class pointer.'))
story.append(P('The `user_demo` command provides a small, direct demonstration of runtime polymorphism. It stores Student and Admin objects through the User interface and invokes overridden virtual methods.'))
story.append(PageBreak())

# 9 algorithm
page('Matching Algorithm and Exchange Workflow','08 — Core logic')
story.append(P('<b>Step 1 — Reciprocal eligibility.</b> For students A and B, A must teach at least one skill B wants, and B must teach at least one skill A wants. If either direction is missing, the pair is not returned.'))
story.append(P('<b>Step 2 — Compatibility score.</b> For an eligible pair, the prototype uses the following transparent heuristic:'))
story.append(P('Score = 0.70 × SkillFit + 0.20 × AvailabilityFit + 0.10 × ModeFit','CodeX'))
bullets(['SkillFit = 100 for a reciprocal pair; non-reciprocal pairs are excluded.','AvailabilityFit = 100 when availability labels match; otherwise 60.','ModeFit = 100 when preferred learning modes match; otherwise 70.'])
story.append(P('For example, a pair with matching availability and mode receives 100. A pair with different availability and mode receives 70 + 12 + 7 = 89. Matches are sorted in descending order using the overloaded Match comparison operator.'))
story.append(P('<b>Step 3 — Exchange workflow.</b> The requester selects a match and creates a Pending request. The recipient can accept or decline it. The new status is persisted to exchanges.csv.'))
story.append(P('<b>Algorithm classification.</b> This is rule-based scoring, not machine learning. Future work could learn weights from ratings or successful exchanges, but that is not implemented in this prototype.'))
story.append(PageBreak())

# 10 UI/data
page('Interface, Storage and Analytics','09 — Implementation')
story.append(P('<b>Interface pages.</b> Overview presents community metrics and the current student’s skill snapshot. Discover displays reciprocal matches and compatibility. My Profile creates or updates a profile. Exchanges shows requests and recipient actions. Analytics visualises the number of students offering and seeking each skill.'))
story.append(P('<b>CSV storage.</b> students.csv stores identity, course, year, skills offered, skills wanted, availability and learning mode. exchanges.csv stores request ID, requester, target, skill, status and creation date. CSV is readable and portable, though it is not suitable for concurrent production workloads.'))
story.append(P('<b>Data analytics.</b> The analytics script transforms semicolon-separated skill lists into long-form observations. It groups by skill and type, counts Offered and Wanted records, and computes Demand gap = Wanted − Offered. It exports a summary CSV and two horizontal bar charts.'))
for fn,cap in [('skills_offered.png','Figure 1. Most offered skills from the included demonstration dataset.'),('skills_wanted.png','Figure 2. Most wanted skills from the included demonstration dataset.')]:
    p=ROOT/'analytics'/'output'/fn
    if p.exists(): story += [Image(str(p),width=76*mm,height=48*mm),P(cap,'Smallx')]
story.append(PageBreak())

# 11 testing
page('Testing and Results','10 — Verification')
story.append(P('The C++ engine was compiled with g++ using the C++17 standard. The automated integration test suite runs the executable against an isolated temporary data directory. The following tests passed in the build environment:'))
table([['Test case','Expected result','Result'],['Sample data initialisation','Seed student records can be loaded','PASS'],['Reciprocal match','S001 discovers reciprocal candidate S002','PASS'],['One-sided overlap','A one-way profile is excluded from reciprocal matches','PASS'],['Exchange lifecycle','Request can be created and status updated','PASS'],['Polymorphism demonstration','Student and Admin virtual behaviour is invoked','PASS'],['Profile update','Existing student record is updated in CSV','PASS']],[48*mm,82*mm,28*mm])
story.append(P('<b>Build verification.</b> The C++ engine compiled successfully and the Python adapter successfully invoked the compiled executable. The analytics script generated the summary CSV and two chart images. Python source files passed syntax compilation.'))
story.append(P('<b>Verification limitation.</b> The Streamlit runtime could not be launched in the isolated build environment because external package downloads were unavailable. Therefore, the browser UI and cloud deployment still require a final run in an environment with the dependencies installed. Do not claim that a public deployment URL has been tested until the team deploys it.'))
story.append(PageBreak())

# 12 conclusion contributions references
page('Conclusion, Contributions and References','11 — Final section')
story.append(P('<b>Conclusion.</b> SkillLoop demonstrates how object-oriented C++ can power the core logic of a practical peer-learning application. The prototype combines an abstract user hierarchy, encapsulated domain objects, overloaded search functions, operator-based match ranking, CSV persistence and a reciprocal compatibility algorithm. Streamlit makes the workflow accessible through a browser, while Python analytics summarises campus skill supply and demand.'))
story.append(P('<b>Future scope.</b> Add secure authentication, a relational database, real-time chat, calendar scheduling, notifications, richer availability overlap, user ratings and feedback-based score calibration. These are proposed extensions, not current features.'))
story.append(P('<b>Individual contributions — confirm before submission.</b>'))
table([['Member','Proposed individual contribution'],['Aman — [ROLL NO.]','C++ class hierarchy and OOP implementation; matching engine and reciprocal scoring; C++/Python adapter; integration tests and technical documentation.'],['Iksha — [ROLL NO.]','Streamlit page layout and interactions; profile and exchange workflow; CSV data validation; analytics and charts; UI test scenarios.'],['Both members','Requirements, design review, sample data, integration review, report and viva preparation.']],[36*mm,122*mm])
story.append(P('<b>References</b>'))
refs=['ISO C++ Foundation, C++ documentation: https://isocpp.org/','Streamlit documentation: https://docs.streamlit.io/','Python documentation: https://docs.python.org/3/','Pandas documentation: https://pandas.pydata.org/docs/','Matplotlib documentation: https://matplotlib.org/stable/','CMake documentation: https://cmake.org/documentation/']
for r in refs: story.append(P('• '+r,'Smallx'))
story.append(P('<b>Submission checklist:</b> replace all bracketed identity placeholders; verify the contribution split; add the final GitHub repository and deployed demo URL after testing; attach genuine application screenshots if required by the faculty guide.','Smallx'))

def footer(canvas,doc):
    canvas.saveState(); w,h=A4
    if doc.page>1:
        canvas.setStrokeColor(colors.HexColor('#E4E1EF'));canvas.line(20*mm,15*mm,w-20*mm,15*mm)
        canvas.setFont('Tinos',8);canvas.setFillColor(colors.HexColor('#77768A'))
        canvas.drawString(20*mm,10*mm,'SkillLoop | Project Report')
        canvas.drawRightString(w-20*mm,10*mm,f'Page {doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=19*mm,bottomMargin=22*mm,title='SkillLoop Project Report',author='SkillLoop Project Team')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
