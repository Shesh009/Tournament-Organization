import math
import os
import random
from tabulate import tabulate


def over_to_balls(overs):
    return (round(math.modf(overs)[0],1)*10+math.modf(overs)[1]*6)

def balls_to_overs(balls):
    return (balls//6+(balls%6)/10)

class Node:
    def __init__(self,team,opp,runs,wickets,played,conceeded,taken,bowled,num,max_overs,toss,decision):
        self.team=team
        self.opp=opp
        self.s_runs=runs
        self.s_wickets=wickets
        self.s_played=played
        self.s_conceeded=conceeded
        self.s_taken=taken
        self.s_bowled=bowled
        self.runs=runs
        self.wickets=wickets
        self.played=played
        self.b_played=over_to_balls(played)
        self.v_played=max_overs if self.wickets==10 else played
        self.conceeded=conceeded
        self.taken=taken
        self.bowled=bowled
        self.b_bowled=over_to_balls(bowled)
        self.v_bowled=max_overs if self.taken==10 else bowled
        self.result=str(team if runs>conceeded else opp)
        self.max_overs=max_overs
        self.match=num
        self.toss=toss
        self.decision=decision
        self.prev=None
        self.next=None

class Team:
    def __init__(self,team):
        self.head=Node(team," ",0,0,0,0,0,0,0,0,None,None)
        self.tail=Node(team," ",0,0,0,0,0,0,0,0,None,None)
        self.head.next=self.tail
        self.tail.prev=self.head

    def insert(self,team,opp,runs,wickets,played,conceeded,taken,bowled,num,max_overs,toss,decision):
        if self.head is None:
            new_node=Node(team,opp,runs,wickets,played,conceeded,taken,bowled,num,max_overs,toss,decision)
            self.head.next=new_node
            new_node.prev=self.head
            new_node.next=self.tail
            self.tail.prev=new_node
            return
        new_node=Node(team,opp,runs,wickets,played,conceeded,taken,bowled,num,max_overs,toss,decision)

        new_node.runs+=self.tail.prev.runs
        new_node.wickets+=self.tail.prev.wickets
        new_node.played=balls_to_overs(self.tail.prev.b_played+over_to_balls(played))
        new_node.conceeded+=self.tail.prev.conceeded
        new_node.bowled=balls_to_overs(self.tail.prev.b_bowled+over_to_balls(bowled))
        new_node.taken+=self.tail.prev.taken
        p=max_overs if wickets==10 else played
        new_node.v_played=balls_to_overs(over_to_balls(self.tail.prev.v_played)+over_to_balls(p))
        b=max_overs if taken==10 else bowled
        new_node.v_bowled=balls_to_overs(over_to_balls(self.tail.prev.v_bowled)+over_to_balls(b))
        new_node.b_played+=self.tail.prev.b_played
        new_node.b_bowled+=self.tail.prev.b_bowled

        new_node.prev=self.tail.prev
        self.tail.prev.next=new_node
        self.tail.prev=new_node
        new_node.next=self.tail

    def search(self,team,opp):
        if self.head.next==self.tail:
            # print("No match is scheduled")
            return False
        temp=self.head.next
        while temp is not self.tail:
            if temp.team.upper()==team.upper() and temp.opp.upper()==opp.upper():
                return [temp.runs,temp.conceeded]
            temp=temp.next
        return False

    def tail_prev(self):
        print(self.tail.team.upper())
        print("Total Runs scored : ",str(self.tail.prev.runs))
        print("Total wickets lost : ",str(self.tail.prev.wickets))
        print("Total Overs played : ",str(self.tail.prev.played))
        print("Total balls played : ",str(self.tail.prev.b_played))
        print("Total overs played virtually : ",str(self.tail.prev.v_played))
        print("Total Runs conceeded : ",str(self.tail.prev.conceeded))
        print("Total overs bowled : ",str(self.tail.prev.bowled))
        print("Total wickets taken : ",str(self.tail.prev.taken))
        print("Total overs bowled virtually : ",str(self.tail.prev.v_bowled))
        print("Total balls bowled : ",str(self.tail.prev.b_bowled))

    def printing(self):
        temp=self.head.next
        if temp is self.tail:
            print("No match is completed of this team")
        while temp is not self.tail:
            # data=[]
            # print("Match",str(temp.match))
            # print(temp.team.upper()+" "*(25-len(temp.team))+"vs"+" "*(25-len(temp.opp))+temp.opp.upper()+"Toss Winner"+"Toss decision"+" "*25+"WINNER"+" "*25+"MAX_OVERS")
            # print(str(temp.s_runs)+"/"+str(temp.s_wickets)+"("+str(temp.s_played)+")"+" "*(38-len(temp.team)),end="")
            # print(str(temp.s_conceeded)+"/"+str(temp.s_taken)+"("+str(temp.s_bowled)+")"+temp.toss+temp.decision,end="")
            # print(22*" "+temp.result.upper()+30*" "+str(temp.max_overs))
            # print()
            print("Match",str(temp.match))
            print("-----------------------")
            data=[]
            data.append([(str(temp.s_runs)+"/"+str(temp.s_wickets)+"("+str(temp.s_played)+")")," ",str(temp.s_conceeded)+"/"+str(temp.s_taken)+"("+str(temp.s_bowled)+")"
                         ,temp.toss,temp.decision,temp.result,temp.max_overs])
            print(tabulate(data,headers=[temp.team.upper(),"vs",temp.opp.upper(),"Toss Winner","Toss Decisison","Winner","Max_Overs"]))
            print("\n\n")
            # data.append([temp.team.upper(),temp.opp.upper(),///////])
            temp=temp.next

    def no_of_matches(self):
        temp=self.head.next
        mat=0
        win=0
        s=""
        while temp is not self.tail:
            mat+=1
            if temp.team==temp.result:
                win+=1
                s+="W "
            else:
                s+="L "
            temp=temp.next
        return [mat,win,mat-win,s[-10:]]

    
    def nrr(self):
        n=self.tail.prev.runs/self.tail.prev.v_played-self.tail.prev.conceeded/self.tail.prev.v_bowled
        n=str(n)
        if n[0]!="-":
            n="+"+n
        return n[:6]
    
def find_key_by_value(dictionary, value_to_find):
    for key, value in dictionary.items():
        if value[1] == value_to_find:
            return value[0]
    return "No such Team"

class Match:
    def __init__(self,matchno,team1,runs1,wickets1,overs1,team2,runs2,wickets2,overs2,max_overs,toss,decision):
        self.matchno=matchno
        self.team1=team1
        self.runs1=runs1
        self.wickets1=wickets1
        self.overs1=overs1
        self.team2=team2
        self.runs2=runs2
        self.wickets2=wickets2
        self.overs2=overs2
        self.max_overs=max_overs
        self.toss=toss
        self.decision=decision
        self.winner="Match yet to be done."

class Matches:
    def __init__(self):
        self.head=Match(0," ",0,0,0," ",0,0,0,0,None,None)
        self.tail=Match(0," ",0,0,0," ",0,0,0,0,None,None)
        self.head.next=self.tail
        self.tail.prev=self.head

    def insert(self,matchno,team1,team2,max_overs,toss,decision):
        if self.head is None:
            new_node=Match(matchno,team1,0,0,0,team2,0,0,0,max_overs,toss,decision)
            self.head.next=new_node
            new_node.prev=self.head
            new_node.next=self.tail
            self.tail.prev=new_node
            return
        new_node=Match(matchno,team1,0,0,0,team2,0,0,0,max_overs,toss,decision)
        new_node.prev=self.tail.prev
        self.tail.prev.next=new_node
        self.tail.prev=new_node
        new_node.next=self.tail

    def edit(self,matchno,team1,runs1,wickets1,overs1,team2,runs2,wickets2,overs2,max_overs,Team_dict,toss,decision):
        temp=self.search(team1,team2)
        if temp is None:
            print("No match is scheduled between these teams")
            return
        temp.runs1=runs1
        temp.runs2=runs2
        temp.wickets1=wickets1
        temp.wickets2=wickets2
        temp.overs1=overs1
        temp.overs2=overs2
        temp.toss=toss
        temp.decision=decision
        if runs1==0 and runs2==0:
            temp.winner="Match yet to be done."
        elif runs1==runs2:
            temp.winner="Match Drawn"
        elif runs1>runs2:
            temp.winner=team1
        else:
            temp.winner=team2
        x=find_key_by_value(Team_dict,team1)
        y=find_key_by_value(Team_dict,team2)
        if runs1!=0 and runs2!=0 and overs1!=0 and overs2!=0 and x.search(team1,team2)==False and y.search(team2,team1)==False:
            x.insert(team1,team2,runs1,wickets1,overs1,runs2,wickets2,overs2,matchno,max_overs,toss,decision)
            y.insert(team2,team1,runs2,wickets2,overs2,runs1,wickets1,overs1,matchno,max_overs,toss,decision)

    def search(self,team,opp):
        if self.head.next==self.tail:
            print("No match is scheduled")
            return None
        temp=self.head.next
        while temp is not self.tail:
            if temp.team1.upper()==team.upper() and temp.team2.upper()==opp.upper():
                return temp
            temp=temp.next

    def printing(self):
        temp=self.head.next
        if temp is self.tail:
            print("No matches are scheduled")
        while temp is not self.tail:
            print("Match",str(temp.matchno))
            print("-----------------------")
            # print(temp.team1.upper()+" "*(25-len(temp.team1))+"vs"+" "*(25-len(temp.team2))+temp.team2.upper()+" "*15+"Toss winner"+" "*15+"Toss decision"+" "*25+"WINNER"+" "*25+"MAX_OVERS")
            # print(str(temp.runs1)+"/"+str(temp.wickets1)+"("+str(temp.overs1)+")"+" "*(38-len(temp.team1)),end="")
            # print(str(temp.runs2)+"/"+str(temp.wickets2)+"("+str(temp.overs2)+")"+" "*18+temp.toss+" "*18+temp.decision,end="")
            # print(" "*22+temp.winner.upper()+" "*24+str(temp.max_overs))
            # print()
            data=[]
            data.append([(str(temp.runs1)+"/"+str(temp.wickets1)+"("+str(temp.overs1)+")")," ",str(temp.runs2)+"/"+str(temp.wickets2)+"("+str(temp.overs2)+")"
                         ,temp.toss,temp.decision,temp.winner,temp.max_overs])
            print(tabulate(data,headers=[temp.team1.upper(),"vs",temp.team2.upper(),"Toss Winner","Toss Decisison","Winner","Max_Overs"]))
            print("\n\n")
            temp=temp.next

def Enter_Teams(teams,Team_dict):
    n=int(input(" no.of teams : "))
    for i in range(1,n+1):
        x=input("Enter team name : ")
        teams.append(x)
        Team_dict[i][1]=x

def write_to_file(matches):
    fp=open("C:/Users/Medha Trust/Desktop/SHESHU/Projects/Tournament Orgranization/Tournament/schedule.txt","a")
    fp.write("matchno,team1,runs1,wickets1,overs1,team2,runs2,wickets2,overs2,toss,decision,max_overs\n")
    for i in range(len(matches)):
        x=[i+1,matches[i][0],0,0,0,matches[i][1],0,0,0,"not_completed","not_completed",20]
        for j in x:
            fp.write(str(j))
            if x.index(j)!=len(x)-1 or i==19:
                fp.write(",")
        fp.write("\n")
    fp.close()

def insert_to_LL(m,matches):
    for i in range(len(matches)):
        m.insert(i+1,matches[i][0],matches[i][1],20,"toss not completed","-")

def schedule(teams,m):
    random.shuffle(teams)
    if len(teams)%2!=0:
        teams.insert(0,"Empty")
    matches = []
    num_teams = len(teams)

    for j in range(num_teams - 1):
        mid = num_teams // 2
        for i in range(mid):
            match = [teams[i], teams[num_teams - i - 1]]
            if match[0]!="Empty" and match[1]!="Empty":
                matches.append(match)
        teams.insert(1, teams.pop())
    try:
        teams.remove("Empty")
    except:
        teams=teams
    
    write_to_file(matches)
    insert_to_LL(m,matches)
    
    return matches

def table(d,teams):
    tab=[]
    for i in teams:
        x=find_key_by_value(d,i).no_of_matches()
        if x[0]==0:
            tab.append([i.upper()+" "*(14-len(i)),0,0,0,0*2,0,0])
        else:
            tab.append([i.upper()+" "*(14-len(i)),x[0],x[1],x[2],x[1]*2,x[3],float(find_key_by_value(d,i).nrr())])
    tab=sorted(tab,key=lambda x:x[0])
    tab=sorted(tab,key=lambda x:(x[4],x[6]),reverse=True)
    # for i in tab:
    #     print(i[0]+"\t"+str(i[1])+"\t"+str(i[2])+"\t"+str(i[3])+"\t"+str(i[4])+"\t"+str(i[5])+(13-len(str(i[5])))*" "+str(i[6]))
    print(tabulate(tab,headers=['TEAM','MAT','WON','LOST','POINTS','STREAK','NRR']))

def score_editing(m,Team_dict,teams):
    fp=open("C:/Users/Medha Trust/Desktop/SHESHU/Projects/Tournament Orgranization/Tournament/schedule.txt","r")
    lines=fp.readlines()
    for i in lines[3:]:
        j=i.split(",")
        m.insert(int(j[0].strip()),j[1].strip(),j[5].strip(),int(j[11].strip()),j[9].strip(),j[10].strip())
    for i in lines[3:]:
        j=i.split(",")
        m.edit(int(j[0].strip()),j[1].strip(),
                    int(j[2].strip()),int(j[3].strip()),float(j[4].strip()),j[5].strip()
                    ,int(j[6].strip()),int(j[7].strip()),float(j[8].strip()),int(j[11].strip()),Team_dict,j[9].strip(),j[10].strip())
    table(Team_dict,teams)

def over():
    Team1=Team("Team1")
    Team2=Team("Team2")
    Team3=Team("Team3")
    Team4=Team("Team4")
    Team5=Team("Team5")
    Team6=Team("Team6")
    Team7=Team("Team7")
    Team8=Team("Team8")
    Team9=Team("Team9")
    Team10=Team("Team10")
    Team11=Team("Team11")
    Team12=Team("Team12")
    Team13=Team("Team13")
    Team14=Team("Team14")
    Team15=Team("Team15")
    Team_dict={1:[Team1,""],2:[Team2,""],3:[Team3,""],4:[Team4,""],5:[Team5,""],
        6:[Team6,""],7:[Team7,""],8:[Team8,""],9:[Team9,""],10:[Team10,""],
        11:[Team11,""],12:[Team12,""],13:[Team13,""],14:[Team14,""],15:[Team15,""]}
    
    m=Matches()
    teams=[]
    fp=open("C:/Users/Medha Trust/Desktop/SHESHU/Projects/Tournament Orgranization/Tournament/schedule.txt","r")
    x=fp.readlines()
    fp.close()
    try:
        s=x[1].split(",")
        tour=x[0]
        print("Existing Teams : ")
        for i in s:
            print(i)
    except:
        print("Create a tournament by entering No\n")
        tour=""
    if input(f"Want to continue with "+tour.strip()+" tournament (Yes/No) : ")=="No":
        os.system("cls")
        name=input("Enter the tournament name : ")
        Enter_Teams(teams,Team_dict)
        fp=open("C:/Users/Medha Trust/Desktop/SHESHU/Projects/Tournament Orgranization/Tournament/schedule.txt","w")
        fp.write(name)
        fp.write("\n")
        for i in teams:
            fp.write(i)
            if i==teams[-1]:
                fp.write("\n")
            else:
                fp.write(",")
        fp.close()
        matches=schedule(teams,m)
        os.system("cls")
        print("Matches are scheduled for above teams.")
        input()
        print("\n\n")
    else:
        fp=open("C:/Users/Medha Trust/Desktop/SHESHU/Projects/Tournament Orgranization/Tournament/schedule.txt","r")
        lines=fp.readlines()
        for i in lines[1:2]:
                j=i.strip().split(",")
                for k in range(len(j)):
                    teams.append(j[k])
                    Team_dict[k+1][1]=j[k]
        fp.close()

    def points_table():
        os.system('cls')
        m=Matches()
        score_editing(m,Team_dict,teams)
        print("\n\n")
        return m
    
    print("\n\n")
    m=points_table()

    while True:
        print("\t\tMENU")
        print("\t--------------------")
        print("\t1.MATCHES SCHEDULE\n\t2.POINTS TABLE\n\t3.EACH TEAM COMPLETED MATCHES\n\t4.EXIT")
        n=int(input("\tEnter your option : "))
        os.system('cls')
        if n==1:
            m.printing()
            print("\n\n")
        elif n==2:
            points_table()
        elif n==3:
            try:
                x=input("Enter team : ")
                os.system("cls")
                find_key_by_value(Team_dict,x).printing()
            except:
                print("No such team")
            print("\n\n")
        else:
            break

os.system("cls")
over()