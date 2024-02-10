import csv
from datetime import date
from datetime import date
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist
from .models import StudentTb,StudentTbSerializer , GroupLinkTb
from .utils import send_message,download_file
from .funtion_utily import create_group,load_grp_his
from .ai_file import process_chat



from django.conf import settings
access_token = settings.ACCESS_TOKEN


## Process The Input Of User From Chat
def process_data(data):
    text = data.get('text','')
    if not text.startswith('/'):
        return
    
    if text.startswith('/addfile'):
        file_id = data.get('attachments',[])[0]['file_id']
        group_id  = data.get('group_id','')
        url = 'https://file.groupme.com/v1/{}/files/{}?access_token={}&omit-content-disposition=false'.format(group_id,file_id,access_token)
        status,msg = download_file(url=url)

        if status :
            with open(msg, 'r') as file:
                reader = csv.DictReader(file)                
                for row in reader:
                    year = row['year']
                    class_section = row['class_section']

                    uid = row.pop('uid', None)                    
                    grp_link_obj = GroupLinkTb.objects.filter(year=year, class_section=class_section)

                    if not grp_link_obj.exists():
                        grp_link = create_group(f"{class_section } {year} Batch Group")
                        grp_link_obj = GroupLinkTb.objects.create(
                        year=year,
                        class_section=class_section,
                        grp_link=grp_link)
                        row['grp_link'] = grp_link_obj

                    student, created = StudentTb.objects.update_or_create(uid=uid,defaults=row)
            return msg
        else :
            send_message(f"Error {msg}")
            return  False
        
    
    elif text.startswith('/ask'):
        question = text.split()[1:]
        question = ''.join(question)
        chat_data = load_grp_his(99214826)
        answer = process_chat(chat_data,question)
        send_message(f"{answer}")
        return
    elif text.startswith('/timetable'):
        uuid = text.split()[1]
        print(uuid)
        if uuid != '8376':
            send_message(f"Invalid Student Id {uuid}.Please Check You Student Id")
            return

        send_message(f"Your Time Table","https://i.groupme.com/1009x766.jpeg.c3ed9a6fa53e4810a610b62d82a94032")
        return
    elif text.startswith('/course'):
        uuid = text.split()[1]
        print(uuid)
        if uuid != '8376':
            send_message(f"Invalid Student Id {uuid}.Please Check You Student Id")
            return

        send_message(f"Your Time Table","https://i.groupme.com/1088x789.jpeg.91a03b3f6f1e409cb504a33e3bbe6d0b")

        return

    elif text.startswith('/announcement'):
        uuid = text.split()[1]
        print(uuid)
        if uuid != '8376':
            send_message(f"Invalid Student Id {uuid}.Please Check You Student Id")
            return

        today = date.today()

        msg= f"""📣 Announcement {today}📣

                Dear Students,

                Good news! The college will be closed for a delightful 2-day holiday starting tomorrow. Enjoy the break, recharge, and return refreshed for another productive academic week. Happy holidays! 🌟
            """
        send_message(f"{msg}")

        return

    elif text.startswith('/assignment'):
        uuid = text.split()[1]
        print(uuid)
        if uuid != '8376':
            send_message(f"Invalid Student Id {uuid}.Please Check You Student Id")
            return

        today = date.today()

        msg= f"""Assignment 1:
                Explore the impact of climate change on biodiversity. Write a 3-page essay with examples of endangered species and propose solutions.

                Assignment 2:
                Compare two historical events from different regions or time periods in a 4-page analysis, highlighting similarities, differences, and societal impacts.

                Assignment 3:
                Conduct a case study on a successful entrepreneur, covering challenges, strategies, and lessons learned. Present findings in a 5-page report with relevant data.

                Assignment 4:
                Examine the influence of technology on education in a 2-page reflection. Discuss advantages, challenges, and provide examples and opinions.
                            """
        send_message(f"{msg}")

        return
    elif text.startswith('/help'):
        help_message = """
        Available commands:
        /ask <question> - Ask a question and get a response.
        /timetable <student_id> - Get the timetable for a student.
        /course <student_id> - Get the courses for a student.
        /announcement <student_id> - View announcements for a student.
        /assignment <student_id> - View assignments for a student.
        /mydetail - Get your details.
        
        Example usage:
        /ask How does climate change affect biodiversity?
        /timetable 8376
        /course 8376
        /announcement 8376
        /assignment 8376
        /mydetail
        """
        send_message(help_message)
        return



    elif text.startswith('/mydetail'):
        text        = text.split()
        student_id  = text[1]
        try:
            student_obj = StudentTb.objects.get(uid=student_id)
            serializer = StudentTbSerializer(student_obj)            
            print(serializer.data['grp_link']['grp_link'])
        except ObjectDoesNotExist:
            return f'Sorry No Student Found With {student_id}'
        "We are excited to have you join the {} group for the {student_obj.year} Batch."
        message = "Hey, {}!\n\nWe are excited to have you join the {} group for the {} Batch. class for the upcoming semester. 🎉 To kick off this new chapter, we've created a dedicated group where you can connect with your classmates, share resources, and stay updated on important announcements.\n\nJoin the {} group now to start engaging with your peers: {}\n\nWe can't wait to see all that you'll accomplish in this new class!\n\nBest regards,\n[Your College Name] Administration".format(student_obj.name,student_obj.class_section,student_obj.year ,student_obj.class_section, serializer.data['grp_link']['grp_link'])
        return message
        return 'Hey Dear "{}" Your Section is\n "{}" for 2022 Batch \n Here Is the Link To Join The Official Group of your Batch \n {}'.format(student_obj.name,student_obj.class_section,serializer.data['grp_link']['grp_link'])

    # return "No Command"



class LostAndFound(APIView):
    def post(self, request, format=None):
        # send_message('msg')
        data = request.data

        text = data.get('text','')
        grp_id = data.get('group_id','')
    
        if text.startswith('/ask'):
            question = text.split()[1:]
            question = ''.join(question)
            chat_data = load_grp_his(grp_id)
            answer = process_chat(chat_data,question)
            send_message(f"{answer}")
            return
        return Response({'status' : True ,'message' : f'Company Created Saved successfully ' , 'data' : data})



class ProcessIncomingMsg(APIView):
    def post(self, request, format=None):
        # send_message('msg')
        print("InReq")
        data = request.data
        print("InReq",data)
        msg = process_data(data) 
        if msg :
            send_message(msg)
        return Response({'status' : True ,'message' : f'Company Created Saved successfully ' , 'data' : data})




class ProcessIncomingMsgDirect(APIView):
    def post(self, request, format=None):
        print("InReq Direct ")
        data = request.data
        print(f"{data=}")
        # send_message("from view")
        return Response({'status' : True ,'message' : f'Company Created Saved successfully ' , 'data' : data})
