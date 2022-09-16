import pandas as pd

def pointx_to_resolutionx(xinput,map_of_games,resX=1024):
    df_map_adjustement = pd.read_csv ("C:/Users/thibault/cs_go_project/map_adjustement/map_data.csv")
    startX=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["StartX"].values
    endX=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["EndX"].values
    try:
        sizeX=endX-startX
        if startX < 0:
            xinput += startX *(-1.0)
        else:
            xinput += startX
        xoutput = float((xinput / abs(sizeX)) * resX)
        return xoutput
    except:
        print(xinput)

def pointy_to_resolutiony(yinput,map_of_games,resY=1024):
    df_map_adjustement = pd.read_csv ("C:/Users/thibault/cs_go_project/map_adjustement/map_data.csv")
    startY=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["StartY"].values
    endY=df_map_adjustement[df_map_adjustement["map"]==map_of_games]["EndY"].values
    try:
        sizeY=endY-startY
        if startY < 0:
            yinput += startY *(-1.0)
        else:
            yinput += startY
        youtput = float((yinput / abs(sizeY)) * resY)

        return resY-youtput
    except:
        print(yinput)

def get_coord_dataframe(map_select,dic_list,x,y,text,info):
    dataframe_position_final = pd.DataFrame(columns=['x', 'y'])

    #if text:
     #   dataframe_position_final = pd.DataFrame(columns=['x', 'y',str(info)])
    for element in dic_list:
        information = []
        X = element[x]
        Y = element[y]
        if text:
            for i in info:
                information.append(element[i])
            information_str = ','.join(str(e) for e in information)
        else:
            information_str = None
        dataframe_position_final = position_coordonate(dataframe_position_final,map_select,X,Y,text,information_str,info)
    return dataframe_position_final

def position_coordonate(dataframe_position_final,map,x,y,text,information,info):
    x_correct = pointx_to_resolutionx(x,map)
    y_correct = pointy_to_resolutiony(y,map)
    dataframe_position = pd.DataFrame([[x_correct,y_correct]],columns=['x','y'])
    if text:
        dataframe_position = pd.DataFrame([[x_correct, y_correct,information]], columns=['x', 'y','info'])
    return  dataframe_position_final.append(dataframe_position).reset_index(drop=True)