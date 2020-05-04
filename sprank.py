import sqlite3

conn=sqlite3.connect('spider.sqlite')
cur=conn.cursor()

from_ids=list()
cur.execute('SELECT DISTINCT from_id FROM Links')
for row in cur:
    from_ids.append(row[0])


to_ids=list()
links=list()
cur.execute('SELECT DISTINCT from_id,to_id FROM Links')
for row in cur:
    from_id=row[0]
    to_id=row[1]
    if from_id not in from_ids: continue
    if from_id==to_id: continue                    #to check if the the link is backlink
    if to_id not in from_ids: continue             #to ensure that the page link is retrieved already.
    links.append(row)
    if to_id not in to_ids: to_ids.append(to_id)


prev_ranks=dict()
for node in from_ids:
    cur.execute('SELECT new_rank FROM Pages WHERE id=?',(node,))
    row=cur.fetchone()[0]
    prev_ranks[node]=row                                        #mapping new_rank with their respective ids 

ival=input('Enter The Number of Iterations')
many=1
if(int(ival)>1):many=int(ival)

if len(prev_ranks)<1: print('Nothing to page rank')

for i in range(many):
    next_ranks=dict()
    total=0.0
    for (node,old_rank) in list(prev_ranks.items()):
        total=total+old_rank
        next_ranks[node]=0.0                                     #inserting from_ids into new_ranks

    for (node,old_rank) in list(prev_ranks.items()):
        give_ids=list()                                        #to store the outbound links
        for (from_id,to_id) in links:
            if from_id!=node:continue
            if to_id not in to_ids:continue
            give_ids.append(to_id)
        if(len(give_ids)<1):continue
        amount=old_rank/len(give_ids)                  #here amount determines the contribution of the present page to the page rank of its outbound links
                                                       
        for id in give_ids:
            next_ranks[id]=next_ranks[id]+amount          #the contribution is added(accumulated) to the outbound page 

    newtotal=0    
    for (node,next_rank) in list(next_ranks.items()):
        newtotal=newtotal+next_rank

    evap=(total-newtotal)/len(next_ranks)                       #Evaporating the rank of pages having no follow attribute(1.0)in ur case 

    for (node,next_rank) in list(next_ranks.items()):
        next_ranks[node]=next_ranks[node]+evap                 #passing on the evap value to each rank


    totdiff=0
    for (node,old_rank) in list(prev_ranks.items()):
        next_rank=next_ranks[node]
        diff=abs(old_rank-next_rank)
        totdiff=totdiff+diff
    
    avgdiff=totdiff/len(prev_ranks)
    print(i+1,avgdiff)
    
    prev_ranks=next_ranks

print(list(next_ranks.items())[:5])

cur.execute('UPDATE Pages SET old_rank=new_rank')
for (id,new_rank) in list(next_ranks.items()):
    cur.execute('UPDATE Pages SET new_rank=? WHERE id=?',(new_rank,id))
conn.commit()
cur.close()






