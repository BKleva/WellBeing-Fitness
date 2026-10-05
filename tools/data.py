"""Content for the WellBeing Fitness site: team, class styles, services, FAQs.

All facts come from the studio's existing Wix site (wellbeing-fitness.com). Edit here, then run:  python tools/build.py
"""

# --------------------------------------------------------------------------------------------------
# Team.  tags drive the filter chips on /team/.  img = file stem in /images (team-*.webp) or None.
# --------------------------------------------------------------------------------------------------
TEAM = [
    dict(name="Scott Cassa", role="Founder · Fitness & Wellness", tags=["fitness", "recovery"], img="scott-cassa",
         short="Founder and trainer of 20+ years; specialist in corrective exercise, oncology exercise and fitness for fragile health.",
         bio=["Scott founded WellBeing Fitness after more than twenty years as a trainer. He holds certifications through the National Academy of Sports Medicine and Harvard Medical School's Executive Education program for Health and Wellness, and is a Certified Advanced Cancer Exercise Specialist through the Cancer Exercise Training Institute.",
              "He specializes in private personal training, group wellness, corrective exercise, weight-loss management, athletic strength and conditioning, post-physical-therapy and cardiac-rehab fitness, oncology exercise, brain-injury fitness resources and corporate wellness, and enjoys supporting adaptive sports and fitness for youth and adults.",
              "A brain-injury survivor in his teens, Scott helps clients overcome health setbacks to stay strong in body and mind. He is a father of two and a nine-time competitor in the Mount Washington Race to the Summit."]),
    dict(name="Melissa Matheson", role="Fitness, Nutrition, Athletics & Wellness", tags=["fitness", "nutrition"], img="melissa-matheson",
         short="Master Health & Nutrition Coach and Certified Menopause Coaching Specialist; multiple-time Boston Marathon qualifier.",
         bio=["Melissa is a NASM Certified Personal Trainer with a Master's Health and Nutrition Coaching certification through Precision Nutrition, plus an RRCA Running Coach credential and a Certified Menopause Coaching Specialist designation.",
              "She specializes in personal training, nutrition, health and wellness coaching, women's health, group and youth fitness, and designs wellness workshops for corporate clients. An avid runner, Melissa has qualified for and run the Boston Marathon multiple times."]),
    dict(name="Ron Rigazio", role="Fitness & Athletics", tags=["fitness"], img="ron-rigazio",
         short="NASM-certified strength and conditioning coach focused on quality of movement, stabilization and agility.",
         bio=["Ron's strength and conditioning programs focus on quality of movement, stabilization and agility, adapted to every fitness level.",
              "After a back injury pulled him away from weight training, a trainer showed him how to strengthen his back, glutes and hamstrings and move correctly. Pain-free and energized, Ron left the corporate world to help others overcome similar challenges. Outside the studio he coaches youth sports and spends time with family."]),
    dict(name="Meghan Kwartler", role="Yoga · Personal Training · Lifestyle Wellness", tags=["yoga", "fitness"], img="meghan-kwartler",
         short="300-hour trained yoga teacher and NASM trainer weaving anatomy, movement science and mindfulness together.",
         bio=["Meghan began her 200-hour teacher training with Anusara in 2011 and completed it in 2019. She is certified in Love Your Brain yoga (accessible yoga for those with brain injuries), recently completed a 300-hour advanced training with Heart and Bones Yoga Studio, and holds a NASM Personal Training certification.",
              "She teaches privately and in groups, including in corporate settings, and loves weaving embodied anatomy, movement science and mindfulness into her teaching."]),
    dict(name="Chris Kandianis", role="Pilates · Yoga", tags=["pilates", "yoga"], img="chris-kandianis",
         short="STOTT Pilates certified in mat and reformer; studying Pilates since 2004 and yoga since 2000.",
         bio=["Chris has studied Pilates since 2004 and yoga since 2000, and loves helping people build the strength and flexibility to enjoy sports and to prevent and overcome injury. She is STOTT Pilates certified in Matwork and Reformer and an RYT 200 yoga instructor, with added training in injuries, special populations and anatomy.",
              "Since opening her own studio in 2006 she has taught thousands of classes and worked with hundreds of clients. She holds a BA from Tufts University and an MBA from Simmons College."]),
    dict(name="Brenda Doben", role="Pilates · Group & Private Reformer", tags=["pilates"], img="brenda-doben",
         short="Power Pilates Comprehensive instructor and TRX-certified; teaches whole-food plant-based cooking.",
         bio=["Brenda became a Power Pilates Comprehensive Certified Instructor in 2022 after Pilates helped her overcome chronic neck and lower-back pain. She brings a thoughtful, holistic approach to every session and is also certified in TRX Suspension Training.",
              "Beyond the studio she creates recipes and teaches whole-food plant-based cooking classes."]),
    dict(name="Nancy Bonanno", role="Pilates · Barre", tags=["pilates"], img="nancy-bonanno",
         short="Longtime dance-studio owner and former professional dancer certified in Power Pilates Mat and Reformer.",
         bio=["Nancy owned and directed The Dance Center in Winchendon, MA for 29 years and trained at the Boston Conservatory. Her twenty years as a professional dancer include television specials, music videos and commercials, and performances with Impulse Dance Company and at the Boston Opera House.",
              "She came to Pilates after a hip replacement and is certified in Power Pilates Mat 1 and 2 and Pilates Reformer."]),
    dict(name="Julia", role="Private Pilates Reformer · Barre", tags=["pilates"], img=None,
         short="Pilates reformer and Barre instructor with a dance-education degree; opened The BarreRoom in 2019.",
         bio=["Julia is a certified Pilates reformer and Barre instructor whose ballet and modern-dance background and degree in dance education gave her the foundation for Pilates and Barre. She holds certifications in several Barre methods, including Booty Barre and Piloxing, as well as Pilates Reformer and Mat.",
              "She opened her private training studio, The BarreRoom, in 2019 and is known for thoughtfully crafted classes that emphasize alignment, mobility and active flexibility. Julia lives in Groton with her husband and two daughters."]),
    dict(name="Lisa Siemaszko", role="Barre · Pilates · Fitness", tags=["pilates", "fitness"], img="lisa-siemaszko",
         short="AFAA- and NASM-approved Barre instructor known for energizing, beat-driven playlists.",
         bio=["Lisa discovered Barre in 2019 and became a certified instructor at ASANA in Charlestown in 2020, with training approved by AFAA and NASM. A passionate runner, she first turned to Barre to reduce joint stress and quickly fell in love with how it challenges body and mind.",
              "Known for beat-driven playlists, Lisa creates a welcoming space that is as fun and motivating as it is effective."]),
    dict(name="Nancy Slocum", role="Personal Training · Yoga", tags=["fitness", "yoga"], img="nancy-slocum",
         short="25 years in fitness; customized programming built on the mind-muscle-motion connection.",
         bio=["Nancy has spent 25 years in the fitness industry as a personal trainer, fitness coach and yoga teacher. She designs programs for professional and weekend athletes, marathoners, baby boomers and seniors, combining anatomy, biomechanics, kinesiology, specialized weight training, yoga and meditation.",
              "Her philosophy: whether you're starting out, leveling up or recovering, the first step is to learn how your muscular system is functioning, then build a routine around it. Her motto is “Make Good Health a Habit.”"]),
    dict(name="Dan DiGiacomo", role="Fitness", tags=["fitness"], img="dan-digiacomo",
         short="NASM trainer, corrective exercise specialist and ACE health coach who loves getting desk workers moving.",
         bio=["Dan has coached fitness since 2019 and loves empowering sedentary workers to unchain from the desk. Through engaging, tailored workouts he helps clients rediscover the joy of movement.",
              "He is a NASM-certified personal trainer and corrective exercise specialist and an ACE-certified health coach. Away from the studio he plays hockey, hikes in the White Mountains and travels."]),
    dict(name="Shagufta Rahmen", role="Yoga · Reiki", tags=["yoga", "recovery"], img="shagufta-rahmen",
         short="Vinyasa teacher with a Yin approach; offers Reiki healing sessions in Groton.",
         bio=["Shagufta came to yoga in college and found a mentor in Kripalu teacher Barbara Rich, whose meditative, breath-focused sequencing shaped her practice. She completed her 200-hour Yoga Alliance Fluid Yoga certification in 2016 and Yin Yoga teacher training in 2018.",
              "Her classes are Vinyasa Flow in style with a Yin approach that centers mindfulness and breath, creating a restorative time for mind, body and spirit."]),
    dict(name="Melissa Ackerman", role="Yoga · Yin · Chair Yoga · Yoga Nidra", tags=["yoga"], img="melissa-ackerman",
         short="500-hour RYT with 25+ years of practice; certified in Yin, Chair Yoga and Yoga Nidra.",
         bio=["Melissa has practiced yoga for over 25 years. She completed her 200-hour training in 2019 at Revolution Community Yoga and her 300-hour certification in 2025 through YogaRenew, and is certified in Yin Yoga, Chair Yoga and Yoga Nidra.",
              "Her classes encourage students to use the breath as a bridge between body and mind and to meet themselves where they are."]),
    dict(name="MacKenzie Fitzgerald", role="Yoga · Sound Meditation", tags=["yoga", "recovery"], img="mackenzie-fitzgerald",
         short="Yoga teacher and certified sound-healing practitioner leading grounding classes and sound baths.",
         bio=["MacKenzie holds a 200-hour yoga certification and multiple sound-healing certifications, including through the Complementary Medical Association. She brings both structure and softness to her teaching.",
              "Her classes and sound baths are designed to feel grounding, welcoming and safe, a place to arrive exactly as you are."]),
    dict(name="Erica Cahill", role="Yoga · Live Music", tags=["yoga"], img="erica-cahill",
         short="500-hour RYT, anatomy educator and musician who weaves live music into class.",
         bio=["Erica is a 500-hour RYT, musician and self-described anatomy nerd. She completed her 200-hour training in 2010 and 300-hour training in 2015, and co-facilitates 200-hour programs through Sacred Seeds Yoga School, where she developed an anatomy module.",
              "Her teaching is rooted in the belief that what we practice grows stronger, and she often weaves live music into class."]),
    dict(name="Eleonora Cordovani", role="Yoga Therapy · Yoga for Cancer & Parkinson's", tags=["yoga", "recovery"], img="eleonora-cordovani",
         short="Trauma-informed yoga teacher and yoga-therapist intern serving cancer and Parkinson's communities.",
         bio=["Eleonora is a Yoga Alliance certified teacher with more than 500 hours of training and is currently a yoga therapist intern. All of her classes are trauma-informed and inclusive for every body.",
              "She specializes in yoga therapy, yoga for cancer and yoga for Parkinson's, and brings a background in the arts, having studied theater therapy in Italy."]),
    dict(name="Violet Young", role="Yoga", tags=["yoga"], img="violet-young",
         short="200-hour teacher trained in vinyasa, hatha, restorative and fusion; gravitates to power flow.",
         bio=["Violet has practiced yoga for over five years and holds a 200-hour certificate, with mentorship in vinyasa, hatha, restorative and fusion classes. She loves a power-flow class that challenges your yogi edge. Off the mat she hikes in the White Mountains of NH, reads and takes photographs."]),
    dict(name="Jason Brady", role="Yoga", tags=["yoga"], img="jason-brady",
         short="Fluid Yoga–trained teacher whose flows build heat with intentional movement; all levels welcome.",
         bio=["Jason completed his 200-hour training with Fluid Yoga. His teaching focuses on mind, body and breath with intentional movement: classes that flow while building heat and welcome every level. He loves the outdoors, music and animals."]),
    dict(name="Val Templeton", role="Yoga · Slow Flow", tags=["yoga"], img="val-templeton",
         short="Slow-flow specialist who leaves students calm, grounded and restored.",
         bio=["Val found yoga 25 years ago and finished her 200-hour training at Revolution Community Yoga in 2023, adding an assisting certification in 2024. Her specialty is slow flow that leaves you feeling calm, grounded and restored. She loves reading, hiking, the beach, family and her dog, Hooper."]),
    dict(name="Darleen Murray", role="Yoga · Slow Flow & Restorative", tags=["yoga"], img="darleen-murray",
         short="25+ years of practice; grounded, welcoming slow-flow and restorative classes.",
         bio=["Darleen brings over 25 years of personal practice to her teaching. She completed her 200-hour training at Windsoul Wellness Center in 2019 and focuses on slow flow and restorative yoga, inviting students to move mindfully, explore each posture with curiosity and carry that calm into daily life."]),
    dict(name="Denise LeGrow", role="Yoga · Gentle Flow", tags=["yoga"], img="denise-legrow",
         short="Gentle-flow teacher offering encouragement, exploration and compassion.",
         bio=["Denise discovered yoga during her first pregnancy and completed her 200-hour training at Revolution Community Yoga in 2023. Her gentle flow classes offer a space of encouragement, exploration and compassion."]),
    dict(name="Megan Willwerth", role="Yoga", tags=["yoga"], img="megan-willwerth",
         short="Teacher and mother of two who loves sharing the philosophy and benefits of yoga.",
         bio=["Megan found yoga on a whim about fifteen years ago, began studying its philosophy a decade ago, and found a love of teaching during her 200-hour training. A mother of two teenagers, she enjoys the arts, the forest and tending her garden."]),
    dict(name="Krista Simon, MPT", role="Physical Therapy · Body and Sole PT", tags=["recovery"], img="krista-simon",
         short="Physical therapist with nearly 30 years of experience, on-site at our Westford studio.",
         bio=["Krista is the founder of Body and Sole Physical Therapy Services and brings nearly 30 years of experience to the WellBeing community. She began her practice in New York City focused on endurance athletes and active adults and is known for an integrative, whole-body approach.",
              "She is especially passionate about working with runners, active older adults and women in midlife, and is a certified menopause coaching specialist."]),
]

TEAM_FILTERS = [("all", "Everyone"), ("fitness", "Personal training"), ("yoga", "Yoga"), ("pilates", "Pilates & Barre"),
                ("nutrition", "Nutrition"), ("recovery", "Recovery & therapy")]

# --------------------------------------------------------------------------------------------------
# Group class styles (from the studio's class-description page)
# --------------------------------------------------------------------------------------------------
CLASS_STYLES = [
    dict(name="Slow Flow", group="yoga", level="Beginner friendly", text="Poses are held longer to build muscular endurance, with conscious breathing and meditative movement to release tension and clear the mind."),
    dict(name="Gentle Yoga", group="yoga", level="Beginner friendly", text="A soothing practice of stretching and relaxation at a slow, deliberate pace, with modifications offered throughout."),
    dict(name="All Levels", group="yoga", level="All levels", text="A creative, breath-linked flow that increases flexibility and tones muscle. Props and variations let you meet yourself where you are."),
    dict(name="Hatha", group="yoga", level="Some experience helpful", text="A strong, dynamic practice that builds strength of body and mind and leaves you invigorated."),
    dict(name="Vinyasa", group="yoga", level="Some experience helpful", text="Breath and movement combine in a flowing sequence of poses, building strength and flexibility."),
    dict(name="Yin", group="yoga", level="All levels", text="Seated and reclined postures held two to five minutes let joints and fascia release. A meditative way to reduce stress and anxiety."),
    dict(name="Restorative", group="yoga", level="Beginner friendly", text="Fully supported by props in a candlelit room, with hands-on assistance and gentle massage. No experience necessary."),
    dict(name="Mindful Flow", group="yoga", level="All levels", text="Poses held for multiple breaths to release the legs, hips, back and shoulders while working muscles throughout the body."),
    dict(name="Kundalini", group="yoga", level="All levels", text="A 60-minute morning practice of kriyas, breathwork, flow and mantra to move energy through the body."),
    dict(name="Yoga Sculpt", group="yoga", level="Active", text="Upbeat cardio, yoga poses and hand weights to build lean muscle and boost metabolism."),
    dict(name="Teen Yoga", group="yoga", level="Ages 11–19", text="A slow-paced, confidence-building practice of strength, flexibility and conscious breathing for teens."),
    dict(name="Pilates Mat-1", group="pilates", level="Beginner friendly", text="A foundational series for whole-body strength and a stable core: better posture, balance, flexibility and coordination."),
    dict(name="Pilates with Weights", group="pilates", level="All levels", text="Pilates and standing balance work with 2–5 lb hand weights or weighted balls for toning and core stability."),
    dict(name="Yoga Pilates Fusion", group="pilates", level="All levels", text="Pilates stability for the shoulders, core and pelvis, paced like a yoga class with standing and balance poses."),
    dict(name="Barre Fitness", group="pilates", level="All levels", text="A low-impact, full-body workout blending ballet, Pilates, yoga and strength training with precise, repetitive movements."),
    dict(name="Barre Cardio Fusion", group="pilates", level="Active", text="Low-impact cardio, light-weight sculpting, barre work for leg toning, core work and stretching."),
]

# --------------------------------------------------------------------------------------------------
# Reformer Pilates packages (from the studio's intro-sale flyer; confirm before launch)
# --------------------------------------------------------------------------------------------------
REFORMER_MONTHLY = [
    dict(name="8 sessions / month", price="$680", note="Best for 2× per week", badge="Top choice",
         perks=["Monthly auto-renew", "10% off group programs", "3-month minimum commitment", "1 friends & family pass per month", "One pause per year on request"]),
    dict(name="4 sessions / month", price="$360", note="Best for 1× per week", badge="",
         perks=["Monthly auto-renew", "10% off group programs", "3-month minimum commitment"]),
]
REFORMER_PACKS = [
    dict(name="6 sessions", price="$510", per="$85 / session", note="2-month expiration", badge=""),
    dict(name="12 sessions", price="$960", per="$80 / session", note="4-month expiration", badge="Most popular"),
    dict(name="24 sessions", price="$1,800", per="$75 / session", note="8-month expiration", badge="Lowest per session"),
]
REFORMER_SINGLE = dict(name="Single session", price="$95", note="Assessment included")

# --------------------------------------------------------------------------------------------------
# Services.  Each entry builds one page.
# --------------------------------------------------------------------------------------------------
SERVICES = [
    dict(
        slug="personal-training", nav="Personal Training", card="Personal Training", img="private-training",
        icon="dumbbell", locs="Westford · Groton",
        title="Personal Training in Westford & Groton, MA | WellBeing Fitness",
        desc="Private & small-group personal training in Westford and Groton, MA. NASM-certified trainers for strength, weight loss, corrective exercise & rehab fitness.",
        eyebrow="Private fitness", h1="Find your <em>health-first</em> mindset.",
        lede="Stay focused on your goals with the support, motivation and accountability of an experienced fitness and lifestyle wellness expert. Train on your own or bring up to three friends.",
        short="One-to-one and small-group training designed around your goals, history and abilities.",
        img_alt="Two people holding a plank side by side during a training session",
        facts=[("Format", "1:1 or groups of 2–4"), ("Where", "Westford & Groton"), ("Pricing", "By package"), ("First step", "Free consultation")],
        focus=["Strength training", "Weight management", "Corrective exercise", "Cardiovascular health", "Restorative mobility", "Athletic & sport-specific conditioning",
               "Post-injury & post-physical-therapy fitness", "Cardiac rehab fitness", "Fitness for fragile health status", "Brain-injury fitness resources", "Adaptive sports & fitness"],
        sections=[
            ("Programs built around the whole person", [
                "Every client is an individual, with their own goals, interests, health history and fitness level. That's the heart of our whole-life model, and it's why your program starts with you rather than a template.",
                "Clients may book appointments individually or in a group of two to four participants. Programs are designed to suit your personal needs and abilities so you can achieve your goals, feel your best, stay ahead of your health and get everything you want out of life."]),
        ],
        steps=[("Talk with us", "Book a free consultation call to share your goals, history and schedule."),
               ("Choose your package", "Pricing is based on the package you select. We'll recommend a rhythm that fits your goals and your life."),
               ("Train with a plan", "Work one-to-one or with a small group in our Westford or Groton studio, with your program adapting as you progress.")],
        team=["Scott Cassa", "Melissa Matheson", "Ron Rigazio", "Meghan Kwartler", "Nancy Slocum", "Dan DiGiacomo"],
        faq=[("How much does personal training cost?", "Pricing is based on the package you select. Request a free consultation and we'll walk you through the options that suit your goals."),
             ("Can I train with a friend or partner?", "Yes. Clients may book individually or in a group of two to four participants."),
             ("What is the cancellation policy?", "A 24-hour cancellation is required for all personal fitness and wellness appointments. Cancelling with less notice results in the loss of a session from your package."),
             ("What should I bring?", "Please bring a change of shoes for training sessions at the Westford studio. Complimentary water is provided for private fitness participants."),
             ("Do you work with injuries or health conditions?", "Our team has experience with post-physical-therapy and cardiac-rehab fitness, oncology exercise, brain-injury fitness resources and fitness for fragile health status. Tell us about your history during your consultation.")],
        related=["nutrition-coaching", "oncology-exercise", "recovery"], interest="Personal Training",
    ),
    dict(
        slug="pilates", nav="Pilates & Barre", card="Private Pilates", img="reformer",
        icon="ring", locs="Westford · Groton",
        title="Reformer & Mat Pilates in Westford, MA | WellBeing Fitness",
        desc="Private reformer and mat Pilates plus group Pilates and Barre classes in Westford and Groton, MA. Build core strength, posture and flexibility.",
        eyebrow="Pilates & Barre", h1="Strength that starts <em>at your core.</em>",
        lede="Pilates builds core strength, improves posture and increases flexibility through focused, controlled movement. Choose private reformer or mat sessions, or join a group class.",
        short="Private reformer and mat sessions, plus group Pilates and Barre classes for every level.",
        img_alt="Pilates reformer machine with a padded box in a bright studio",
        facts=[("Private", "Reformer, mat or both"), ("Packages", "6, 12 or 24 sessions"), ("Group", "Mat, weights, Barre"), ("Where", "Westford & Groton")],
        focus=["Core strength & stability", "Posture & alignment", "Balance, control & body awareness", "Active flexibility", "Injury prevention & recovery", "Beginner to advanced"],
        sections=[
            ("Private sessions, tailored to you", [
                "Private sessions offer customized workouts with your choice of Reformer, Mat work, or a combination of the two, expertly guided toward your goals. With focused one-to-one attention you progress faster, refine your technique and stay motivated, and flexible scheduling makes it easy to stay consistent.",
                "Our private Pilates instructors accept clients by appointment. Message us to schedule a first session or a package of 6 or 12 sessions."]),
            ("Group Pilates & Barre classes", [
                "Prefer the energy of a class? Our schedule includes Pilates Mat-1, Pilates with Weights, Yoga Pilates Fusion, Barre Fitness and Barre Cardio Fusion, all with modifications so beginners and experienced movers can train side by side."]),
        ],
        steps=[("Message us", "Tell us your goals and preferred studio. We'll match you with an instructor."),
               ("Start with a first session", "Single sessions include an assessment so your instructor can plan around your body."),
               ("Choose a rhythm", "Pick a monthly membership or a 6-, 12- or 24-session package, and book your sessions.")],
        team=["Brenda Doben", "Nancy Bonanno", "Julia", "Chris Kandianis", "Lisa Siemaszko"],
        faq=[("Do I need experience to try Pilates?", "No. Exercises adapt to every fitness level, so beginners and experienced participants are equally welcome."),
             ("What's the difference between reformer and mat Pilates?", "Mat Pilates uses your body weight on the floor. Reformer work uses a spring-resistance machine that adds support and challenge. Private sessions can use either or blend the two."),
             ("How do I book a private Pilates session?", "Use the booking button or message info@wellbeing-fitness.com. We'll help you find an instructor and a time that works."),
             ("Do you offer packages?", "Yes. See our memberships page for reformer Pilates monthly plans and 6-, 12- and 24-session packages.")],
        related=["personal-training", "recovery", "womens-wellness"], interest="Private Pilates", show_reformer=True,
    ),
    dict(
        slug="nutrition-coaching", nav="Nutrition & Health Coaching", card="Health Coaching & Nutrition", img="nutrition-bowl",
        icon="leaf", locs="In person · Zoom",
        title="Nutrition & Health Coaching in Westford, MA | WellBeing Fitness",
        desc="Health and nutrition coaching in Westford, MA, in person or on Zoom. Fuel Your Life programs, a free 30-minute consult and meal prep at 15% off.",
        eyebrow="Health coaching & nutrition", h1="Small changes. <em>Lasting</em> health.",
        lede="What we put into our bodies affects how we think, feel, act, move and sleep. Our coaching helps you build long-term, sustainable habits, one small step at a time.",
        short="Fuel Your Life coaching, small-group programs and chef-prepared weekly meal prep.",
        img_alt="Colorful bowl of fresh vegetables, eggs and avocado",
        facts=[("Coach", "Melissa Matheson"), ("Format", "In person or Zoom"), ("Start", "Free 30-min consult"), ("Meal prep", "15% off with MEALPREP15")],
        focus=["Nutrition", "Movement", "Sleep", "Stress", "Self-care"],
        sections=[
            ("Fuel Your Life Health & Nutrition Coaching", [
                "We'll be by your side on a journey to discover your strengths and the areas where small changes can make a big difference: nutrition, movement, sleep, stress and self-care. The Fuel Your Life program helps you reach your goals and maintain them by building changes into your daily routine that become a lifestyle.",
            ]),
        ],
        includes=["Weekly 30-minute sessions with your coach, in person or on Zoom", "A recap and additional resources sent after every session", "Access to a database of recipes for healthy inspiration", "Unlimited text and email support from your coach"],
        steps=[("Free consultation", "In a 30-minute conversation we talk about your goals and break them into small daily actions."),
               ("Pick your program", "Choose one-to-one Fuel Your Life coaching or the small-group version. Not sure? We'll help you choose or customize."),
               ("Fuel your life", "Meet weekly, get recaps and recipes, and lean on unlimited coach support between sessions.")],
        extra=("Meal prep, made easy", [
            "WellBeing Nutrition Programs has teamed up with Coleman Catering and Salt & Light Cafe Bistro for a weekly preorder menu of chef-prepared, nutritious meals. Order online and pick up on Wednesdays and Saturdays during open cafe hours.",
            "WellBeing clients can use code <strong>MEALPREP15</strong> for 15% off."]),
        team=["Melissa Matheson", "Dan DiGiacomo"],
        faq=[("What is the Fuel Your Life program?", "A customized coaching program with weekly 30-minute in-person or Zoom sessions, weekly recaps and resources, a recipe database and unlimited text and email support from your coach."),
             ("Is there a group option?", "Yes. We offer a small-group version of the Fuel Your Life Health & Nutrition Coaching program."),
             ("How do I start?", "Request a free 30-minute health consultation. You can also call 978-496-1846 or email melissa@wellbeing-fitness.com."),
             ("How does the meal prep ordering work?", "Order the weekly chef-prepared menu online through our partners and pick up on Wednesdays or Saturdays during cafe hours. Use code MEALPREP15 for 15% off.")],
        related=["womens-wellness", "personal-training", "corporate-wellness"], interest="Nutrition & Health Coaching",
        ext_cta=("Menu & ordering", "https://www.toasttab.com/catering/coleman-catering-groton-159-main-street/menu/salt%20%26%20light%20%2F%20wellbeing%20fitness%20meal%20prep"),
    ),
    dict(
        slug="womens-wellness", nav="Women's Wellness", card="Women's Wellness", img="womens-wellness",
        icon="heart", locs="Westford · Groton · Virtual",
        title="Peri/Menopause Wellness Coaching in MA | WellBeing Fitness",
        desc="Peri/menopause wellness coaching in Westford, MA, led by a certified menopause specialist. Support for brain fog, hot flushes, weight gain and sleep.",
        eyebrow="Women's health", h1="Navigate midlife with <em>knowledge</em> and support.",
        lede="Perimenopause and menopause can be challenging. Our programs, led by Master Health, Wellness and Menopause Specialist Melissa Matheson, help you regain control of your health and happiness.",
        short="Peri/menopause coaching for brain fog, hot flushes, weight gain, sleep and energy.",
        img_alt="Smiling person making a heart shape with their hands",
        facts=[("Led by", "Melissa Matheson"), ("Credentials", "Certified Menopause Coaching Specialist"), ("Start", "Free consult or health assessment"), ("Also", "Krista Simon, MPT")],
        focus=["Brain fog", "Hot flushes", "Weight gain", "Sleep", "Energy levels", "Strength & bone health", "Stress & mood"],
        sections=[
            ("Tools, support and knowledge", [
                "From managing brain fog, hot flushes and weight gain to improving sleep and energy, we provide the tools, support and knowledge you need to move through the many common, frustrating symptoms of midlife changes.",
                "Reach out for a free consultation or to book a comprehensive health assessment. Our team can pair coaching with strength training, Pilates, yoga and physical therapy for a truly whole-person plan."]),
        ],
        steps=[("Reach out", "Request a free consultation or book a comprehensive health assessment."),
               ("Get your plan", "Combine health coaching, nutrition and movement into one approach shaped around your symptoms and goals."),
               ("Move well through every season", "Layer in training, Pilates, yoga or physical therapy as your needs change.")],
        team=["Melissa Matheson", "Krista Simon, MPT"],
        faq=[("Who leads the women's wellness programs?", "Melissa Matheson, a Master Health, Wellness and Menopause Specialist and Certified Menopause Coaching Specialist. Physical therapist Krista Simon is also a certified menopause coaching specialist."),
             ("What symptoms can coaching help with?", "Our programs support brain fog, hot flushes, weight gain, sleep, energy levels and the other common symptoms of midlife changes."),
             ("How do I get started?", "Request a free consultation or book a comprehensive health assessment with our team.")],
        related=["nutrition-coaching", "personal-training", "recovery"], interest="Women's Wellness",
    ),
    dict(
        slug="oncology-exercise", nav="Oncology Exercise", card="Oncology Exercise", img="oncology",
        icon="shield", locs="Studio · Home · Virtual",
        title="Oncology Exercise Programs in Westford, MA | WellBeing Fitness",
        desc="Cancer exercise programs led by Certified Advanced Cancer Exercise Specialists in Westford, MA. In studio, at home or virtual. Free consultation.",
        eyebrow="Oncology exercise", h1="Focus on what your <em>body can do.</em>",
        lede="Individual and small-group exercise and lifestyle wellness programming for anyone living with or recovering from cancer, led by our Certified Advanced Cancer Exercise Specialist team.",
        short="Safe, effective exercise for anyone living with or recovering from cancer.",
        img_alt="Trainer guiding an older client through a dumbbell exercise",
        facts=[("Led by", "Certified Advanced Cancer Exercise Specialists"), ("Format", "1:1, small group or DIY"), ("Where", "Studio, home or online"), ("First step", "Free consultation")],
        focus=["Strength", "Energy levels", "Sleep", "Mood", "Physical function", "Quality of life"],
        sections=[
            ("Exercise through every stage", [
                "At a time when changes to your health status can push general fitness and wellness to the back burner, we help you focus on what your body can do while improving general wellness at any stage, and following treatments or surgery. Studies show regular, safe and effective exercise for cancer patients and survivors increases strength and improves energy, sleep, mood, physical function and quality of life, while decreasing common side effects.",
                "Following a free consultation you can choose weekly, biweekly or monthly appointments in studio, at home or virtually online. We also offer small groups and do-it-yourself programs written specifically for you with our guidance. Every program style begins with a comprehensive Oncology Exercise Assessment. General fitness and yoga-style offerings are available with our certified oncology wellness team."]),
        ],
        steps=[("Free consultation", "We listen to your story, your health status and what you want from exercise."),
               ("Oncology exercise assessment", "Every program begins with a comprehensive assessment so training is safe and appropriate."),
               ("Your program", "Choose weekly, biweekly or monthly sessions, a small group, or a program written for you to follow independently.")],
        team=["Scott Cassa", "Eleonora Cordovani"],
        faq=[("Who is this program for?", "Anyone living with or recovering from cancer, at any stage of diagnosis, treatment or recovery."),
             ("Where do sessions take place?", "In studio, at your home, or virtually online. Choose what fits your needs as they change."),
             ("Do I need a doctor's approval?", "We always recommend sharing your plans with your care team. Every program starts with a comprehensive Oncology Exercise Assessment."),
             ("Is there a group option?", "Yes. We offer individual sessions, small groups and independent do-it-yourself programs, plus yoga-style offerings.")],
        related=["personal-training", "recovery", "womens-wellness"], interest="Oncology Exercise",
    ),
    dict(
        slug="recovery", nav="Recovery · Reiki · PT", card="Recovery Therapeutics", img="reiki",
        icon="wave", locs="Westford · Groton",
        title="Reiki, Assisted Stretching & Physical Therapy | WellBeing Fitness",
        desc="Reiki, assisted stretching and on-site physical therapy in Westford and Groton, MA. Radiance Wellness Living (cold plunge, sauna, red light) coming soon.",
        eyebrow="Recovery therapeutics", h1="Restore. <em>Recharge.</em> Feel your best.",
        lede="From gentle energy work to hands-on physical therapy, our recovery services help you move better, relax deeper and keep doing what you love.",
        short="Reiki, assisted stretching and on-site physical therapy, with Radiance Wellness Living coming soon.",
        img_alt="Person receiving a Reiki treatment with hands resting gently on their head",
        facts=[("Reiki", "Groton"), ("Assisted stretch", "Westford & Groton"), ("Physical therapy", "Westford, on-site"), ("Coming soon", "Radiance Wellness Living")],
        focus=[],
        subservices=[
            dict(id="reiki", title="Reiki healing", img="reiki", alt="Reiki practitioner's hands resting on a client's head",
                 text=["Reiki is a Japanese energy-healing technique that promotes relaxation and reduces stress and anxiety through gentle touch. Practitioners use their hands to deliver energy to the body, supporting the flow and balance of your energy.",
                       "Many people who receive Reiki report feeling calm, relaxed and connected. Reiki is a complementary practice and should never be used as an alternative to conventional medical care. While it won't treat or cure a medical condition, it is a low-risk practice that may help you relax while undergoing conventional treatment."],
                 cta=("Request a Reiki session", "Reiki"), meta="Available in Groton"),
            dict(id="assisted-stretch", title="Assisted stretch", img="assisted-stretch", alt="Therapist assisting a client with a leg stretch",
                 text=["Assisted stretching is a personalized service designed to enhance flexibility, improve mobility and optimize physical performance. A short initial assessment evaluates your flexibility, limitations and goals, then each session targets specific muscle groups using static stretching, PNF and dynamic stretching.",
                       "Benefits include a wider range of motion, quicker recovery, injury prevention and stress relief. It suits athletes, seniors maintaining mobility, office workers with stiffness from sitting, and anyone who wants to feel better in their body."],
                 cta=("Book assisted stretch", "Assisted Stretch"), meta="Westford & Groton, scheduled by appointment"),
            dict(id="physical-therapy", title="Physical therapy with Krista Simon, MPT", img="physical-therapy", alt="Physical therapist working with a client",
                 text=["Krista Simon of Body and Sole Physical Therapy brings nearly 30 years of experience to our Westford studio. She considers how sleep, stress, nutrition, movement and mindset all influence how we heal, function and feel, and treats the whole system, not just the symptom.",
                       "Her approach is hands-on and collaborative, and she is especially passionate about working with runners, active older adults and women in midlife. As a certified menopause coaching specialist she helps clients move well through every season of life."],
                 cta=("Book with Krista", "Physical Therapy"), meta="On-site at Westford", mailto="Kristasmn@gmail.com"),
        ],
        sections=[],
        radiance=True,
        steps=[], team=["Shagufta Rahmen", "Krista Simon, MPT", "MacKenzie Fitzgerald"],
        faq=[("Is Reiki a substitute for medical care?", "No. Reiki is a complementary practice and should never replace conventional medical care. It's a low-risk way to relax while undergoing conventional treatment."),
             ("Where is assisted stretching offered?", "At both studio locations depending on the day. Message us and we'll help you find a time that works."),
             ("Where is physical therapy offered?", "Krista Simon, MPT of Body and Sole Physical Therapy sees clients on-site at our Westford studio."),
             ("What is Radiance Wellness Living?", "A new recovery and wellness experience coming soon to 100 Boston Rd in Groton, designed to help you restore, recharge and feel your best, with cold plunge, red light therapy, saunas, hyperbaric and compression.")],
        related=["womens-wellness", "personal-training", "oncology-exercise"], interest="Recovery · Reiki · Physical Therapy",
    ),
    dict(
        slug="corporate-wellness", nav="Corporate Wellness", card="Corporate Wellness", img="corporate-meeting",
        icon="briefcase", locs="On-site · Studio",
        title="Corporate Wellness Programs in MA | WellBeing Fitness",
        desc="Corporate wellness in Massachusetts: Roadmap to Wellness, Corporate Club small-group training and on-site fitness, nutrition and stress-relief workshops.",
        eyebrow="Corporate wellness", h1="Build a <em>roadmap to wellness</em> for your workforce.",
        lede="When your employees feel great, productivity soars. Our Roadmap to Wellness gives your team the tools to make lifestyle wellness part of every day.",
        short="The Roadmap to Wellness, Corporate Club training and on-site workshops for your team.",
        img_alt="Business colleagues shaking hands over a desk",
        facts=[("Program", "Roadmap to Wellness"), ("Club", "Up to 8 per class"), ("Plans", "Daily, weekly, monthly"), ("Workshops", "On-site or at the studio")],
        focus=["Small group training", "Group fitness classes", "Nutrition workshops", "Stress-relief clinics", "Meditation workshops", "Stretching & flexibility", "Health coaching & personal training"],
        sections=[
            ("Roadmap to Wellness", [
                "Our robust fitness, nutrition and stress-relief program is fully customizable from a vast selection of offerings, from small-group training and group fitness classes to nutrition workshops, stress-relief clinics, meditation workshops, stretching and flexibility sessions, and individualized health coaching and personal training. Contact us to design a program, including a sample annualized plan."]),
            ("Corporate Club", [
                "Corporate Club clients purchase weekly time slots in small-group training classes of up to eight participants, focused on strength, conditioning, plyometrics and cardiovascular fitness. All fitness levels are welcome, with modifications as needed. Availability is limited."]),
            ("On-site programs", [
                "Our staff can bring fitness, nutrition, stress-relief, stretching and meditation workshops to your office, either woven into the Roadmap or à la carte."]),
        ],
        includes=["Flexible plans: purchase daily, weekly or monthly seats", "Offer seats as incentives for your employees", "Hold dedicated days and times for your staff", "Sample workshops: The Office Stretch & Strengthen, The Business Traveler's Workshop, Reading Food Labels & Ingredient Lists, Stress Relief & Meditation"],
        steps=[("Tell us about your team", "Share your goals, headcount and schedule."),
               ("Design your roadmap", "We'll build a customized program from our menu of workshops, classes and training."),
               ("Launch & support", "Deliver on-site or at our studios, with seats flexible by the day, week or month.")],
        team=["Scott Cassa", "Melissa Matheson", "Meghan Kwartler"],
        faq=[("What is the Roadmap to Wellness?", "A customizable fitness, nutrition and stress-relief program that gives employees the tools to make lifestyle wellness part of each day."),
             ("What is the Corporate Club?", "Small-group training classes of up to eight participants where companies purchase daily, weekly or monthly seats for their employees. Availability is limited."),
             ("Can you come to our office?", "Yes. We offer on-site workshops such as the Office Stretch & Strengthen workshop, stress relief and meditation, and more."),
             ("How do we get started?", "Contact us to discuss your goals. We'll design a program that fits your team.")],
        related=["nutrition-coaching", "personal-training", "recovery"], interest="Corporate Wellness",
    ),
]

# --------------------------------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------------------------------
LOCATIONS = [
    dict(slug="westford", name="Westford", street="203 B Littleton Rd", city="Westford", state="MA", zip="01886",
         img="westford-building", img2="studio-fitness-floor", map_q="203+B+Littleton+Rd,+Westford,+MA+01886",
         title="WellBeing Fitness Westford, MA | Yoga, Pilates & Training",
         desc="WellBeing Fitness Westford at 203 B Littleton Rd, Cornerstone Square: yoga, Pilates, personal training, coaching, oncology exercise and PT. Off Rt. 495.",
         blurb="Our flagship studio is in the Cornerstone Square Shopping Center, directly on Rt. 110 and easily accessible off Rt. 495, right next door to Eastern Bank. It's an innovative, non-intimidating, beautifully designed functional fitness and wellness space.",
         services=["Private Fitness Training", "Health Coaching", "Lifestyle Wellness", "Post Physical Therapy Fitness", "Yoga", "Pilates", "Oncology Exercise", "Physical Therapy (on-site)"],
         notes=[("Parking", "Plenty of direct studio parking with accessible walkways at both entrances."),
                ("Entrances", "Coming for a fitness session? Use the front door. Visiting for yoga or group classes? Use the side group-room entrance."),
                ("Amenities", "Two washrooms and one shower, with complimentary water for private fitness participants."),
                ("Bring", "A change of shoes for training sessions.")],
         near="Cornerstone Square, next to Eastern Bank, on Rt. 110 off Rt. 495"),
    dict(slug="groton", name="Groton", street="134 Main St", city="Groton", state="MA", zip="01450",
         img="groton-building", img2="studio-om-room", map_q="134+Main+St,+Groton,+MA+01450",
         title="WellBeing Fitness Groton, MA | Yoga, Pilates, Barre & Reiki",
         desc="WellBeing Fitness Groton at 134 Main St, next to the Groton Inn: yoga, Pilates, Barre, personal training, Reiki and sound meditation.",
         blurb="Our Groton studio is at 134 Main Street, directly next door to the historic Groton Inn and Forge and Vine restaurant. The entrance is at the back of the building.",
         services=["Personal Training", "Private Groups", "Reiki", "Yoga", "Pilates", "Barre Fitness"],
         notes=[("Parking", "Parking is available along Main Street or behind the building, and overflow parking is across the street in the Prescott Community Center municipal lot."),
                ("Entrance", "Use the entrance at the back of the building."),
                ("Soon nearby", "Radiance Wellness Living is coming soon to 100 Boston Rd, Groton.")],
         near="Next to the historic Groton Inn on Main Street"),
]

# --------------------------------------------------------------------------------------------------
# Site-wide FAQs (home + policies page)
# --------------------------------------------------------------------------------------------------
HOME_FAQ = [
    ("Where are WellBeing Fitness studios located?", "We have two studios in Massachusetts: 203 B Littleton Rd in Westford (Cornerstone Square, off Rt. 495) and 134 Main St in Groton, next to the Groton Inn."),
    ("I'm brand new. Where should I start?", "Request a free consultation and we'll help you choose, or reserve a beginner-friendly class such as Slow Flow, Gentle Yoga, Restorative or Pilates Mat-1. When you book your first class you'll be guided through creating an account and completing a participation waiver."),
    ("How do I register for a class?", "Choose a class on the live schedule, reserve your spot and check your location before you arrive. You can cancel up to two hours before class through your account."),
    ("What should I bring to a group class?", "A mat and water bottle are helpful, but we have mats, water and all the props you need: blankets, blocks and more. Wear whatever feels comfortable to move in."),
    ("Do you offer memberships and class passes?", "Yes: monthly auto-renew memberships with member perks, plus flexible class passes that can be shared with a family member. See our memberships page for details."),
    ("Do you work with people who have injuries or health conditions?", "Yes. Our team has experience with post-physical-therapy and cardiac-rehab fitness, oncology exercise and fitness for fragile health status, and we have a physical therapist on-site in Westford."),
]

POLICY_FAQ = [
    ("How do I register for group classes?", "Sign up on the live class schedule. We have two locations, Groton and Westford, plus online class options. Walk-ins are welcome as long as there is an open spot, but please always check the schedule before heading to the studio to be sure the class is running."),
    ("When should I arrive?", "Arrive at least five minutes before the start of class or session. Classes begin on time, and arriving late may result in a missed class and the loss of a class from your class count."),
    ("What if I need to cancel a group class?", "Class registrations can be canceled by logging into your account up to two hours before class time. If you can't attend and don't cancel, you'll be charged for the spot."),
    ("What if I need to cancel a fitness or wellness appointment?", "A 24-hour cancellation is required for all personal fitness and wellness appointments. Cancelling with less notice results in the loss of a session from your package."),
    ("Do class passes expire?", "Group class, health coaching and fitness training packages each have expiration dates based on the number of classes in the pass. Extension requests can be made along with the purchase of a new package. All sales on class passes and fitness training are final."),
    ("How do unlimited memberships work?", "The Unlimited Monthly Auto Pay membership lists contract details at purchase. Unlimited memberships run on a three-month commitment cycle with auto-renewal, and one one-month pause can be requested within 12 months."),
    ("Is a waiver required?", "Yes. A Client Waiver of Liability must be signed and on file for each participant. You'll complete it when you create your account."),
    ("What are the age requirements?", "Regular weekly classes are for ages 15 and over. Teen and Tween programs are for ages 11 and over."),
    ("What happens in bad weather?", "During winter months, weather-related class cancellations are sent by automatic email or text, based on how you set up your account."),
    ("Where do I park?", "Westford: our main parking lot at 203 B Littleton Road. Groton: in front of the building along Main Street, behind the studio (limited spaces), and in overflow parking across the street at the Prescott Building."),
]

# --------------------------------------------------------------------------------------------------
# Memberships & passes: prices read from the studio's Mindbody online store (site 729963) on 2026-10-05.
# mb = "mindbody" sends the visitor to that store section; "contact" routes to the consultation form
# (packs that are not sold online). Update here if prices change, then rebuild.
# --------------------------------------------------------------------------------------------------
MB_STORE = "https://clients.mindbodyonline.com/asp/main_shop.asp?tabID=3&studioid=729963"
MB_LINK = {"membership": MB_STORE + "&pMode=0", "pass": MB_STORE + "&pMode=1", "gift": MB_STORE + "&pMode=2"}
GROUP_PERKS = ["Every yoga, Pilates, Barre and fitness group class on the schedule", "Westford and Groton studios", "Reserve your spot online in advance"]

PLANS_GROUP = [
    dict(id="single", name="Single class", sub="Pay as you go", price=25, kind="single", size=1, link="pass", mbName="Single Group Class",
         perks=["One group class, any studio", "No commitment", "Perfect for trying a new style"]),
    dict(id="pack5", name="5-class pass", sub="Flexible, shareable", price=110, kind="pack", size=5, valid=4, link="pass", mbName="5 Group Class Pass",
         perks=["Valid for 4 months from purchase", "Share with a family member", "Use at both studios"]),
    dict(id="pack10", name="10-class pass", sub="Flexible, shareable", price=200, kind="pack", size=10, valid=6, link="pass", mbName="10 Group Class Pass",
         perks=["Valid for 6 months from purchase", "Share with a family member", "Use at both studios"]),
    dict(id="pack20", name="20-class pass", sub="Lowest price per class", price=360, kind="pack", size=20, valid=9, link="pass", mbName="20 Group Class Pass",
         perks=["Valid for 9 months from purchase", "Share with a family member", "Use at both studios"]),
    dict(id="m4", name="4 classes / month", sub="Monthly auto-renew", price=80, kind="member", cap=4, link="membership", mbName="4 Classes /$80 Per Month Membership - Auto-Renew",
         perks=["4 group classes each month, based on the current schedule", "Westford and Groton studios", "Reserve your spot online in advance"]),
    dict(id="m8", name="8 classes / month", sub="Monthly auto-renew", price=130, kind="member", cap=8, link="membership", mbName="8 Classes /$130 Per Month Membership - Auto-Renew",
         perks=["8 group classes each month, based on the current schedule", "Westford and Groton studios", "Reserve your spot online in advance"]),
    dict(id="unl", name="Unlimited", sub="Monthly auto-pay", price=140, kind="member", cap=999, link="membership", mbName="Monthly Unlimited Autopay- $140/month",
         perks=["Unlimited group classes at both studios", "Member perks and priority community", "Reserve your spot online in advance"]),
]
TRIAL = dict(name="One-month trial", price=60, note="New to WellBeing? A one-month trial pass for $60, valid for one month from purchase.", mbName="One month trial /$60")

PLANS_PRIVATE = [
    dict(id="m4p", name="4 sessions / month", sub="Monthly auto-renew · about weekly", price=360, per=90, kind="member", freq="weekly", mb="mindbody", link="membership",
         mbName="4 Private Sessions Per Month - Auto-Renew", perks=["Four coached private sessions each month", "Reformer Pilates or personal training", "Westford and Groton studios"]),
    dict(id="m8p", name="8 sessions / month", sub="Monthly auto-renew · twice weekly", price=680, per=85, kind="member", freq="twice", mb="mindbody", link="membership", badge="Top choice",
         mbName="8 Private Sessions Per Month - Auto-Renew", perks=["Eight coached private sessions each month", "10% off group programs", "A friends & family pass each month"]),
    dict(id="p24", name="24-session package", sub="Lowest price per session", price=1800, per=75, kind="pack", freq="flex", mb="mindbody", link="pass", valid=8,
         mbName="Private Training 24 sessions (Westford Private Sessions)", perks=["Valid for 8 months from purchase", "Early-renewal bonus sessions available", "Reformer Pilates or personal training"]),
    dict(id="p12", name="12-session package", sub="Most popular package", price=960, per=80, kind="pack", freq="flex", mb="contact", valid=4, badge="Most popular",
         perks=["Valid for 4 months from purchase", "Early-renewal bonus sessions available", "Booked with our team"]),
    dict(id="p6", name="6-session package", sub="A taste of private training", price=510, per=85, kind="pack", freq="flex", mb="contact", valid=2,
         perks=["Valid for 2 months from purchase", "Booked with our team", "Great for a focused goal"]),
    dict(id="p1", name="Single session", sub="Assessment included", price=95, per=95, kind="single", freq="flex", mb="contact",
         perks=["One private session with an assessment", "Reformer Pilates or personal training", "Booked with our team"]),
]

PLANS_COACH = [
    dict(id="coach", name="3-month coaching program", sub="Health & nutrition coaching", price=340, kind="member", months=3, mb="mindbody", link="membership",
         mbName="3 Month Health Coaching Program", perks=["Three months of one-to-one health and nutrition coaching", "Built around nutrition, movement, sleep, stress and self-care", "Start with a free 30-minute consultation"]),
]
