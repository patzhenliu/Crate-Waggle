from pygame import *

from pygame import *



screen = display.set_mode((600,600))

crate=image.load("crate.jpeg")

display.set_caption("Crate Waggle")
display.set_icon(crate)

crate=transform.scale(crate,(50,50))

backArrow=image.load("backArrow.png")#Icon by Chris Veigt from www.flaticon.com
backArrow=transform.scale(backArrow,(50,50))
backArrowInvert=image.load("backArrowInvert.png")#Icon by Chris Veigt from www.flaticon.com
backArrowInvert=transform.scale(backArrowInvert,(50,50))

levelFile=open("levels.txt","r")

levelList=[]

for i in range(3):
    rowList=[]
    for j in range(10):
        row=levelFile.readline()
        row=row.strip("\n")
        row=row.split(" ")

        rowList.append(row)
    levelList.append(rowList)

def startMenu():
    drawBackground()
    for i in range(3):
        draw.rect(screen,(255,255,255),[200,i*100+200,200,70])
        draw.rect(screen,(0,180,230),[200,i*100+200,200,70],3)

def menuSelect(mx,my,flag):
    mb=mouse.get_pressed()
    if not flag:
        if mb[0]==1:
            flag=True
        if selectPlay(mx,my,mb):
            return "play",flag
        if selectInstruc(mx,my,mb):
            return "instruc",flag
        if selectCredits(mx,my,mb):
            return "credits",flag
    return "menu",flag

def selectPlay(mx,my,mb):
    if Rect(200,0*100+200,200,70).collidepoint(mx,my):
        draw.rect(screen,(0,180,230),[200,0*100+200,200,70])
        if mb[0]==1:
            return True
    
def selectInstruc(mx,my,mb):
    if Rect(200,1*100+200,200,70).collidepoint(mx,my):
        draw.rect(screen,(0,180,230),[200,1*100+200,200,70])
        if mb[0]==1:
            return True

def selectCredits(mx,my,mb):
    if Rect(200,2*100+200,200,70).collidepoint(mx,my):
        draw.rect(screen,(0,180,230),[200,2*100+200,200,70])
        if mb[0]==1:
            return True
    
def levelSelectPage(mx,my,flag):
    drawBackground()
    if backArrowCollide(mx,my):
        return "menu",flag
        
    for i in range(6):
        for j in range(6):
            draw.rect(screen,(255,255,255),[(i+1)*80,(j+1)*80+30,50,50])
            draw.rect(screen,(0,180,230),[(i+1)*80,(j+1)*80+30,50,50],3)
            if Rect((i+1)*80,(j+1)*80+30,50,50).collidepoint(mx,my) and e.type==MOUSEBUTTONDOWN and not flag:
                flag=True
                return str(j*6+i),flag
    return "play",flag

def backArrowCollide(mx,my):
    screen.blit(backArrow,(25,25))
    if Rect(5,5,50,50).collidepoint(mx,my):
        screen.blit(backArrowInvert,(25,25))
        if mb[0]==1:
            return True

def checkLevMouseCollide(mx,my):
    for i in range(6):
        for j in range(6):
            if Rect((i+1)*80,(j+1)*80+30,50,50).collidepoint(mx,my):
                draw.rect(screen,(0,180,230),[(i+1)*80,(j+1)*80+30,50,50])

def drawBackground():
    for i in range(12):
        for j in range(12):
            screen.blit(crate,(i*50,j*50))

def instrucPage(mx,my):
    screen.fill((0,0,0))
    if backArrowCollide(mx,my):
        return "menu"
    return "instruc"

def drawBoard(board,levNum,mx,my):
    drawBackground()
    for i in range(10):
        for j in range(10):
            if board[i][j]=="e":
                draw.rect(screen,(200,200,200),[(j+1)*50+1,(i+1)*50+1,49,49])
            if board[i][j]=="b":
                draw.rect(screen,(0,180,230),[(j+1)*50+1,(i+1)*50+1,49,49])
            if board[i][j]=="s":
                draw.rect(screen,(0,180,230),[(j+1)*50+1,(i+1)*50+1,49,49])
                draw.circle(screen,(255,0,0),((j+1)*50+1+25,(i+1)*50+1+25),20)
                sPos=[i,j]
        
    return levNum,sPos

def moveChar(board,levNum,mx,my,sPos):
    levelBoard=[]
    for i in range(10):
        levelBoard.append(board[i])
    keys=key.get_pressed()
    i,j=sPos
    if keys[K_LEFT] and levelBoard[i][j-1]!="x":
        levelBoard[i][j]="b"
        #if board[i][j+1]=="b":
        levelBoard[i][j-1]="s"
        
    elif keys[K_RIGHT] and levelBoard[i][j+1]!="x":
        levelBoard[i][j]="b"
        #if board[i][j+1]=="b":
        levelBoard[i][j+1]="s"
        
    elif keys[K_UP] and levelBoard[i-1][j]!="x":
        board[i][j]="b"
        #if board[i][j+1]=="b":
        board[i-1][j]="s"
    
    elif keys[K_DOWN] and levelBoard[i+1][j]!="x":
        levelBoard[i][j]="b"
        #if board[i][j+1]=="b":
        levelBoard[i+1][j]="s"
             
    return

page="menu"
flag=False

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        
    keys=key.get_pressed()
    mb = mouse.get_pressed()
    mx,my=mouse.get_pos()

    if mb[0]==0:
        flag=False

    if page=="menu":
        startMenu()
        page,flag=menuSelect(mx,my,flag)

    #print(page)

    if page=="play":
        page,flag=levelSelectPage(mx,my,flag)
        checkLevMouseCollide(mx,my)

    if page!="play" and page!="menu" and page!="instruc" and page!="credits":
        #print(int(page))
        page,sPos=drawBoard(levelList[int(page)],int(page),mx,my)
        moveChar(levelList[int(page)],int(page),mx,my,sPos)
        if backArrowCollide(mx,my):
            page="play"
        

    if page=="instruc":
        page=instrucPage(mx,my)
##
##    if page=="credits":
##        "We are really sorry for this dumb game..."
##        "It's ummm.... really crappy"
##        "Click anywhere for another game that's totally not"
##        "pointless and actually has a goal to achieve..."
##
##        "But srsly... sorry for this uncreative game"

    display.flip()

quit()
