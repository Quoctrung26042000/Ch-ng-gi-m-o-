import psycopg2

# con = psycopg2.connect(database="postgres", user="postgres", password="123", host="localhost", port="5432")
con = psycopg2.connect(database="test1", user="pi", password="hthuan04", host="huuthuanbk.ddns.net", port="5432")


# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.23 #baseline 0.23
EYE_AR_CONSEC_FRAMES = 3

# eye landmarks
eye_landmarks = "model_landmarks/shape_predictor_68_face_landmarks.dat"
# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0


id = [0, 1 , 2]
names = [ 'None', 'Trung','Hoang']
