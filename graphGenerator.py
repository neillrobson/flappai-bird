#%%
import base64
import matplotlib.pyplot as plt
import numpy as np
import json
from ast import literal_eval

data1encoded = 'eyJkZGFFbmFibGVkIjpmYWxzZSwiZGF0YSI6W3sic3RhcnRUaW1lIjoxNjE5MTM3MjUxMzg1LCJkdXJhdGlvbiI6NjQ1Miwic2NvcmUiOjAsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX0seyJzdGFydFRpbWUiOjE2MTkxMzcyNjMwMDYsImR1cmF0aW9uIjo3NTYwLCJzY29yZSI6MCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTEzNzI3NTI0NywiZHVyYXRpb24iOjEyNzQ4LCJzY29yZSI6NCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTEzNzI5ODc5OSwiZHVyYXRpb24iOjczOTcsInNjb3JlIjowLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3MzEwNzQxLCJkdXJhdGlvbiI6MTUyNTAsInNjb3JlIjo1LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTM3MzMxMDg0LCJkdXJhdGlvbiI6MjYyNjgsInNjb3JlIjoxMiwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjEyfSx7InN0YXJ0VGltZSI6MTYxOTEzNzM2MTc0NiwiZHVyYXRpb24iOjkxNzAsInNjb3JlIjoxLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3Mzc1Mjg1LCJkdXJhdGlvbiI6MTI2MzEsInNjb3JlIjozLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3MzkyMzM1LCJkdXJhdGlvbiI6MjA0MjcsInNjb3JlIjo3LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTM3NDE3MTMyLCJkdXJhdGlvbiI6OTQwNSwic2NvcmUiOjEsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxMzc0MzA3MjgsImR1cmF0aW9uIjoxNjAxNiwic2NvcmUiOjUsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX0seyJzdGFydFRpbWUiOjE2MTkxMzc0NjEwNDUsImR1cmF0aW9uIjo4MTU2LCJzY29yZSI6MCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTEzNzU1Njk1NCwiZHVyYXRpb24iOjg2NzIsInNjb3JlIjoxLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3NTY5NzA4LCJkdXJhdGlvbiI6MTIwNDAsInNjb3JlIjozLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTM3NTg2MjU1LCJkdXJhdGlvbiI6MTI3NTIsInNjb3JlIjozLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTM3NjAzNzE5LCJkdXJhdGlvbiI6OTM1MCwic2NvcmUiOjEsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxMzc2MTY5OTcsImR1cmF0aW9uIjoxNzczMSwic2NvcmUiOjcsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxMzc2MzkwODMsImR1cmF0aW9uIjo4Nzk3LCJzY29yZSI6MSwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTEzNzY1MjMyNywiZHVyYXRpb24iOjc4OTMsInNjb3JlIjoxLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3NjY1MTMxLCJkdXJhdGlvbiI6Njg1Miwic2NvcmUiOjAsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxMzc2NzYzODcsImR1cmF0aW9uIjo4ODg5LCJzY29yZSI6MSwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjEyfSx7InN0YXJ0VGltZSI6MTYxOTEzNzY4OTEwMiwiZHVyYXRpb24iOjcwMjAsInNjb3JlIjowLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTM3Njk5Nzk3LCJkdXJhdGlvbiI6ODcxNSwic2NvcmUiOjEsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn1dfQ=='
data1bytes = base64.b64decode(data1encoded)
data1 = json.loads(data1bytes.decode('utf8'))

data2encoded = 'eyJkZGFFbmFibGVkIjpmYWxzZSwiZGF0YSI6W3sic3RhcnRUaW1lIjoxNjE5MTg0NTQ1Nzk0LCJkdXJhdGlvbiI6NjMyMiwic2NvcmUiOjAsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxODQ1NzMyMDgsImR1cmF0aW9uIjo2NTQ1LCJzY29yZSI6MCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTE4NDU4NzE3NSwiZHVyYXRpb24iOjY5NjEsInNjb3JlIjowLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTg0NjI2ODk3LCJkdXJhdGlvbiI6MTIzODYsInNjb3JlIjo0LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg0NjY5OTE3LCJkdXJhdGlvbiI6MzA4NjUsInNjb3JlIjoxOCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTE4NDk5NTc0NSwiZHVyYXRpb24iOjc1MjAsInNjb3JlIjoxLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1MDA4MTAzLCJkdXJhdGlvbiI6MTc0NTYsInNjb3JlIjo4LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1Mzg2ODE4LCJkdXJhdGlvbiI6MTA4ODIsInNjb3JlIjozLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1NDk1NTE3LCJkdXJhdGlvbiI6MjA1NzcsInNjb3JlIjoxMCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTE4NTUyMzk3MCwiZHVyYXRpb24iOjE0MjczLCJzY29yZSI6NiwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjEyfSx7InN0YXJ0VGltZSI6MTYxOTE4NTU0NTAwOSwiZHVyYXRpb24iOjY2MDksInNjb3JlIjowLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTg1NTU2OTg2LCJkdXJhdGlvbiI6MTAwMTgsInNjb3JlIjoyLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1NTcxMDg4LCJkdXJhdGlvbiI6MTA3MzcsInNjb3JlIjozLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTg1NTg5MTEyLCJkdXJhdGlvbiI6NjIxMCwic2NvcmUiOjAsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX0seyJzdGFydFRpbWUiOjE2MTkxODU1OTk4MjQsImR1cmF0aW9uIjo3MjAxLCJzY29yZSI6MCwiZ3Jhdml0eSI6MC4yNSwicGlwZUludGVydmFsIjoxNDAwLCJwaXBlaGVpZ2h0Ijo5MCwiY29sbGlzaW9uUG9zaXRpb24iOjExfSx7InN0YXJ0VGltZSI6MTYxOTE4NTYxMTY3MywiZHVyYXRpb24iOjgxMTMsInNjb3JlIjoxLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1NjI0MDAxLCJkdXJhdGlvbiI6ODc4NSwic2NvcmUiOjIsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX0seyJzdGFydFRpbWUiOjE2MTkxODU2MzY4MjMsImR1cmF0aW9uIjoxNTI2NSwic2NvcmUiOjYsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX0seyJzdGFydFRpbWUiOjE2MTkxODU2NTYzNjgsImR1cmF0aW9uIjoyMjg4MSwic2NvcmUiOjEyLCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTg1NjgzNjM3LCJkdXJhdGlvbiI6MTIxNDQsInNjb3JlIjo0LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTJ9LHsic3RhcnRUaW1lIjoxNjE5MTg1Njk5NTgyLCJkdXJhdGlvbiI6MTQyNzMsInNjb3JlIjo2LCJncmF2aXR5IjowLjI1LCJwaXBlSW50ZXJ2YWwiOjE0MDAsInBpcGVoZWlnaHQiOjkwLCJjb2xsaXNpb25Qb3NpdGlvbiI6MTF9LHsic3RhcnRUaW1lIjoxNjE5MTg1NzIwOTkwLCJkdXJhdGlvbiI6ODgzMywic2NvcmUiOjIsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMn0seyJzdGFydFRpbWUiOjE2MTkxODU3MzY1MzAsImR1cmF0aW9uIjoxMDczNywic2NvcmUiOjMsImdyYXZpdHkiOjAuMjUsInBpcGVJbnRlcnZhbCI6MTQwMCwicGlwZWhlaWdodCI6OTAsImNvbGxpc2lvblBvc2l0aW9uIjoxMX1dfQ=='
data2bytes = base64.b64decode(data2encoded)
data2 = json.loads(data2bytes.decode('utf8'))

scores1 = []
gravity1 = []
pipeInterval1 = []
pipeHeight1 = []
for data in data1["data"]:
    scores1.append(data['score'])
    gravity1.append(data['gravity'])
    pipeInterval1.append(data['pipeInterval'])
    pipeHeight1.append(data['pipeheight'])

scores2 = []
gravity2 = []
pipeInterval2 = []
pipeHeight2 = []
for data in data2["data"]:
    scores2.append(data['score'])
    gravity2.append(data['gravity'])
    pipeInterval2.append(data['pipeInterval'])
    pipeHeight2.append(data['pipeheight'])

x = np.arange(1, 24, 1)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(x, scores1, label='JOE')
ax.plot(x, scores2, label='DALTON')

plt.xticks(x)
ax.set_xlabel('Playthrough')
ax.set_ylabel('Score')
ax.set_title('Scores over the playthroughs')
ax.legend()

fig2, ax2 = plt.subplots()  # Create a figure containing a single axes.
ax2.plot(x, gravity1, label='player1')
ax2.plot(x, gravity2, label='player2')

plt.xticks(x)
ax2.set_xlabel('Playthrough')
ax2.set_ylabel('Gravity')
ax2.set_title('Gravity strength over 10 playthroughs')
ax2.legend()

fig3, ax3 = plt.subplots()  # Create a figure containing a single axes.
ax3.plot(x, pipeInterval1, label='player1')
ax3.plot(x, pipeInterval2, label='player2')

plt.xticks(x)
ax3.set_xlabel('Playthrough')
ax3.set_ylabel('Pipe Interval Distance')
ax3.set_title('Pipe interval distance over 10 playthroughs')
ax3.legend()

fig4, ax4 = plt.subplots()  # Create a figure containing a single axes.
ax4.plot(x, pipeHeight1, label='player1')
ax4.plot(x, pipeHeight2, label='player2')

plt.xticks(x)
ax4.set_xlabel('Playthrough')
ax4.set_ylabel('Pipe Height')
ax4.set_title('Pipe height over 10 playthroughs')
ax4.legend()
# %%
import csv
import base64
import matplotlib.pyplot as plt
import numpy as np
import json

data = []
with open('notddaEnabledData.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row[0])

allData = []
for testerData in data:
    dataBytes = base64.b64decode(testerData)
    jsonData = json.loads(dataBytes.decode('utf8'))
    scores = []
    pipeInterval = []
    pipeHeight = []
    i = 0
    for run in jsonData["data"]:
        if(i != 0 and run['pipeInterval'] == 1410.5):
            break
        scores.append(run['score'])
        pipeInterval.append(run['pipeInterval'])
        pipeHeight.append(run['pipeheight'])
        i = i + 1
    xvals = np.arange(1, len(scores) + 1, 1)
    playerData = {"xvals":xvals, "scores":scores, "pipeInterval":pipeInterval, "pipeHeight":pipeHeight}
    allData.append(playerData)


fig, ax = plt.subplots()
ax.set_xlabel('Playthrough')
ax.set_ylabel('Score')
ax.set_title('DDA Enabled Scores')

for i in range(len(allData)):
    ax.plot(allData[i]["xvals"], allData[i]["scores"], label='player' + str(i))
ax.legend()

fig, ax = plt.subplots()
ax.set_xlabel('Playthrough')
ax.set_ylabel('pipeInterval')
ax.set_title('Baseline pipeInterval Distances')

for i in range(len(allData)):
    ax.plot(allData[i]["xvals"], allData[i]["pipeInterval"], label='player' + str(i))
ax.legend()

fig, ax = plt.subplots()
ax.set_xlabel('Playthrough')
ax.set_ylabel('pipeHeight')
ax.set_title('Baseline pipeHeight Distances')

for i in range(len(allData)):
    ax.plot(allData[i]["xvals"], allData[i]["pipeHeight"], label='player' + str(i))
ax.legend()
    



# %%
import csv
import base64
import matplotlib.pyplot as plt
import numpy as np
import json

dataEnabled = []
with open('ddaEnabledData.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        dataEnabled.append(row[0])

dataNotEnabled = []
with open('notddaEnabledData.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        dataNotEnabled.append(row[0])

allDataEnabled = []
for testerData in dataEnabled:
    dataBytes = base64.b64decode(testerData)
    jsonData = json.loads(dataBytes.decode('utf8'))
    scores = []
    pipeInterval = []
    pipeHeight = []
    i = 0
    for run in jsonData["data"]:
        if(i != 0 and run['pipeInterval'] == 1410.5):
            break
        scores.append(run['score'])
        pipeInterval.append(run['pipeInterval'])
        pipeHeight.append(run['pipeheight'])
        i = i + 1
    xvals = np.arange(1, len(scores) + 1, 1)
    playerData = {"xvals":xvals, "scores":scores, "pipeInterval":pipeInterval, "pipeHeight":pipeHeight}
    allDataEnabled.append(playerData)


allDataNotEnabled = []
for testerData in dataNotEnabled:
    dataBytes = base64.b64decode(testerData)
    jsonData = json.loads(dataBytes.decode('utf8'))
    scores = []
    pipeInterval = []
    pipeHeight = []
    i = 0
    for run in jsonData["data"]:
        if(i != 0 and run['pipeInterval'] == 1410.5):
            break
        scores.append(run['score'])
        pipeInterval.append(run['pipeInterval'])
        pipeHeight.append(run['pipeheight'])
        i = i + 1
    xvals = np.arange(1, len(scores) + 1, 1)
    playerData = {"xvals":xvals, "scores":scores, "pipeInterval":pipeInterval, "pipeHeight":pipeHeight}
    allDataNotEnabled.append(playerData)    

fig, ax = plt.subplots()
#plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
ax.set_xlabel('Playthrough')
ax.set_ylabel('Score')
ax.set_title('DDA vs. Baseline Scores')

for i in range(len(allDataEnabled)):
    ax.plot(allDataEnabled[i]["xvals"], allDataEnabled[i]["scores"], label='DDA_Enabled', color='green')

for i in range(len(allDataNotEnabled)):
    ax.plot(allDataNotEnabled[i]["xvals"], allDataNotEnabled[i]["scores"], label='Baseline', color='red')    

handles, labels = plt.gca().get_legend_handles_labels()
labels, ids = np.unique(labels, return_index=True)
handles = [handles[i] for i in ids]
plt.legend(handles, labels, loc='best')
#ax.legend()
# %%
