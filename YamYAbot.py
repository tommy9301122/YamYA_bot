from PTT_jokes import PttJokes
from bot_data import food_a, food_j, food_c, YamYABot_murmur

from colour import Color
import os
import datetime
from datetime import date
import re
import random
import requests
import pandas as pd
import discord
import nekos
client = discord.Client()

# 顏色判斷用
def get_rating_color(beatmap_rating):
    color_list = list(Color("#4FC0FF").range_to(Color("#4FFFD5"),6))+ \
                 list(Color("#4FFFD5").range_to(Color("#7CFF4F"),6))+ \
                 list(Color("#7CFF4F").range_to(Color("#F6F05C"),9))+ \
                 list(Color("#F6F05C").range_to(Color("#FF8068"),18))+ \
                 list(Color("#ff666b").range_to(Color("#FF3C71"),11))+ \
                 list(Color("#FF3C71").range_to(Color("#6563DE"),11))+ \
                 list(Color("#6563DE").range_to(Color("#2a27a1"),6))
    color_list = list(dict.fromkeys([str(i) for i in color_list]))
    rating_list = [1.5+(i/10) for i in range(61)]
    if beatmap_rating<1.5 :
        return('#4FC0FF', '1.5')
    for color, rating in zip(color_list, rating_list):
        if beatmap_rating>=rating and beatmap_rating<(rating+0.1):
            return(color, str(rating))
    if beatmap_rating>7.5 and beatmap_rating<8 :
        return('#2a27a1', '7.5')
    if beatmap_rating>=8 :
        return('#18158E', '8.0+')
    
# 天數換算用
def parse_date(td):
    resYear = float(td.days)/364.0
    resMonth = int((resYear - int(resYear))*364/30)
    resYear = int(resYear)
    resDay = int(td.days-(364*resYear+30*resMonth))
    return str(resYear) + " years " + str(resMonth) + " months and " + str(resDay) + " days."


#當機器人完成啟動時
@client.event
async def on_ready():
    print('目前登入身份：', client.user)
    
    status_w = discord.Status.online  #Status : online（上線）,offline（下線）,idle（閒置）,dnd（請勿打擾）,invisible（隱身）
    activity_w = discord.Activity(type=discord.ActivityType.playing, name="YamYA我把拔")  #type : playing（遊玩中）、streaming（直撥中）、listening（聆聽中）、watching（觀看中）、custom（自定義）

    await client.change_presence(status= status_w, activity=activity_w)
    
    
#當有訊息時
@client.event
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    
    ###################################################### 早安、晚安
    if message.content.lower() == 'gm':
        await message.channel.send('gm (｡･∀･)ﾉﾞ')
    if message.content.lower() == 'gn':
        await message.channel.send('gn (¦3[▓▓]')
        
    ####################################################### 呱YA murmur
    if message.content.lower() == '呱ya':
        await message.channel.send(random.choice(YamYABot_murmur))
        
    
    ####################################################### 代替呱YA講話
    if message.content.lower().startswith('呱ya說 '):
        repeat_mes = message.content.lower().split("呱ya說 ",1)[1]
        
        if int(message.author.id)==378936265657286659 or int(message.author.id)==86721800393740288:
            await message.delete()
            await message.channel.send(repeat_mes)
    
    ###################################################### 訊息中包含 azgod (不分大小寫)
    str_az = re.search(r'[a-zA-Z]{5}', message.content)
    if str_az:
        if str_az.group(0).lower() == 'azgod':
            k = random.randint(0, 1)
            if k == 0:
                await message.channel.send("https://i.imgur.com/PT5gInL.png")
            if k == 1:
                await message.channel.send("AzRaeL isn't so great? Are you kidding me? When was the last time you saw a player can make storyboard that has beautiful special effect, amazing lyrics and geometry. Mapping with amazing patterns, perfect hitsounds and satisfying flow? AzRaeL makes mapping to another level, and we will be blessed if we ever see a taiwanese with his mapping skill and passion for the game again. Amateurre breaks records. Sotarks breaks records. AzRaeL breaks the rules. You can keep your statistics, I prefer the AzGoD.")
    
    
    ###################################################### 笑話
    
    if message.content=='笑話' :
        
        ptt = PttJokes(1)
        joke_class_list = ['笑話','猜謎','耍冷','XD']
        while True:
            try:
                joke_output = ptt.output()
                if joke_output[1:3] in joke_class_list and re.search('http',joke_output) is None:
                    joke_output = re.sub('(\\n){4,}','\n\n\n',joke_output)

                    joke_title = re.search('.*\\n',joke_output)[0]
                    joke_foot = re.search('\\n.*From ptt',joke_output)[0]
                    joke_main = joke_output.replace(joke_title,'').replace(joke_foot,'')
                    break
            except:
                pass
            
        embed = discord.Embed(title=joke_title, description=joke_main)
        embed.set_footer(text=joke_foot)
        await message.channel.send(embed=embed)
    
        
    
    ###################################################### 其他彩蛋
    if message.content=='貼貼' :
        embed=discord.Embed(title="ლ(╹◡╹ლ)")
        embed.set_image(url=nekos.img('cuddle'))
        await message.channel.send(embed=embed)
        
    if message.content=='抱抱' :
        embed=discord.Embed(title="(つ´ω`)つ")
        embed.set_image(url=nekos.img('hug'))
        await message.channel.send(embed=embed)
        
        
    if message.content=='親親' :
        embed=discord.Embed(title="( ˘ ³˘)♥")
        embed.set_image(url=nekos.img('kiss'))
        await message.channel.send(embed=embed)
        
    if message.content=='喵' :
        embed=discord.Embed(title="喵? ο(=•ω＜=)ρ⌒☆")
        embed.set_image(url=nekos.img('ngif'))
        await message.channel.send(embed=embed)
        
    if message.content=='戳' :
        embed=discord.Embed(title="戳~")
        embed.set_image(url=nekos.img('poke'))
        await message.channel.send(embed=embed)
        
        
    if message.content=='笨蛋' :
        embed=discord.Embed(title="バカ")
        embed.set_image(url=nekos.img('baka'))
        await message.channel.send(embed=embed)

    bad_word_list = ['幹','靠北','幹你娘','fuck you 呱ya','fuck 呱ya']
    if message.content.lower() in bad_word_list:
        await message.channel.send(nekos.img('slap'))            
                
    
    ####################################################### 午餐吃什麼?

    #結尾用語
    ending_list = ['怎麼樣?','好吃',' 98','?','']
    
    # 沒有選類別的話就全部隨機: 吃土 2%  中式/台式 50%  日式/美式/意式 50%   
    if message.content=='午餐吃什麼' or message.content=='晚餐吃什麼' :
        eat_dust = random.randint(1, 100)
        if eat_dust <= 2:
            await message.channel.send('還是吃土?')
        else:
            eat_class = random.randint(1, 2)
            if eat_class == 1:
                await message.channel.send(random.choice(food_c)+random.choice(ending_list))
            if eat_class == 2:
                await message.channel.send(random.choice(food_j+food_a)+random.choice(ending_list))


    if message.content.startswith('午餐吃什麼 ') or message.content.startswith('晚餐吃什麼 ') :

        food_class = message.content.split("吃什麼 ",1)[1]

        if food_class=='中式' or food_class=='台式':
            await message.channel.send(random.choice(food_c)+random.choice(ending_list))
        elif food_class=='日式' :
            await message.channel.send(random.choice(food_j)+random.choice(ending_list))
        elif food_class=='美式' :
            await message.channel.send(random.choice(food_a)+random.choice(ending_list))
        else:
            await message.channel.send('º﹃º')
            



    ####################################################### 推薦麻婆最新上傳的圖    
    if message.content.startswith('神麻婆'):
        try:
            mapper = message.content.split("神麻婆",1)[1]
            if mapper[0] == ' ':
                mapper = mapper[1:]
                
            get_beatmaps = requests.get('https://osu.ppy.sh/api/get_beatmaps?k=13a36d70fd32e2f87fd2a7a89e4f52d54ab337a1&u='+mapper).json()
            beatmaps = {}
            num = 0
            for i in get_beatmaps:
                beatmaps[num] = i
                num = num+1
            df_beatmaps  = pd.DataFrame.from_dict(beatmaps, "index")
            
            
            if df_beatmaps.head(1).creator_id.values[0] == '0':
                await message.channel.send('我找不到這位神麻婆的圖;w;')
            else:
                # Rank & Love
                df_beatmaps['status'] = df_beatmaps.approved.map({'1':'Rank','4':'Love'}).fillna('Unrank')

                # 類別ID轉名稱
                df_beatmaps['genre_id'] = df_beatmaps.genre_id.map({'1':'Unspecified',
                                                                    '2':'Video Game',
                                                                    '3':'Anime',
                                                                    '4':'Rock',
                                                                    '5':'Pop',
                                                                    '6':'Other',
                                                                    '7':'Novelty',
                                                                    '8':'Hip Hop',
                                                                    '9':'Electronic',
                                                                    '10':'Metal',
                                                                    '11':'Classical',
                                                                    '12':'Folk',
                                                                    '13':'Jazz'})

                # 語言ID轉名稱
                df_beatmaps['language_id'] = df_beatmaps.language_id.map({'1':'Unspecified',
                                                                          '2':'English',
                                                                          '3':'Japanese',
                                                                          '4':'Chinese',
                                                                          '5':'Instrumental',
                                                                          '6':'Korean',
                                                                          '7':'FrenchItalian',
                                                                          '8':'German',
                                                                          '9':'Swedish',
                                                                          '10':'Spanish',
                                                                          '11':'Polish',
                                                                          '12':'Russian',
                                                                          '14':'Other'})

                # 將title和artist的unicode遺失值用英文補齊
                df_beatmaps['artist_unicode'] = df_beatmaps['artist_unicode'].fillna(df_beatmaps['artist'])
                df_beatmaps['title_unicode'] = df_beatmaps['title_unicode'].fillna(df_beatmaps['title'])

                # 類別、語言 補遺失值
                df_beatmaps['genre_id'] = df_beatmaps['genre_id'].fillna('Unspecified')
                df_beatmaps['language_id'] = df_beatmaps['language_id'].fillna('Unspecified')

                # 欄位資料型態
                df_beatmaps = df_beatmaps.astype({'beatmapset_id':'int64','favourite_count':'int64','playcount':'int64'})
                df_beatmaps['approved_date'] = pd.to_datetime(df_beatmaps['approved_date'], format='%Y-%m-%d %H:%M:%S')
                df_beatmaps['submit_date'] = pd.to_datetime(df_beatmaps['submit_date'], format='%Y-%m-%d %H:%M:%S')
                df_beatmaps['last_update'] = pd.to_datetime(df_beatmaps['last_update'], format='%Y-%m-%d %H:%M:%S')

                # groupby
                df_beatmaps = df_beatmaps.groupby('beatmapset_id').agg({'beatmap_id':'count',
                                                                         'status':'min',
                                                                         'genre_id':'min',
                                                                         'language_id':'min',
                                                                         'title_unicode':'min',
                                                                         'artist_unicode':'min',
                                                                         'approved_date':'min', 
                                                                         'submit_date':'min', 
                                                                         'last_update':'min', 
                                                                         'favourite_count':'min',
                                                                         'playcount':'sum'}).reset_index(drop=False)



                mapper_id = beatmaps[0].get('creator_id')
                mapper_name = requests.get('https://osu.ppy.sh/api/get_user?k=13a36d70fd32e2f87fd2a7a89e4f52d54ab337a1&u='+mapper_id).json()[0].get('username')
                # 年齡
                mapping_age = parse_date(datetime.datetime.now() - df_beatmaps.submit_date.min())
                # 做圖數量
                mapset_count = format( len(df_beatmaps),',')
                rank_mapset_count = format( len(df_beatmaps.loc[(df_beatmaps.status=='Rank')]),',')
                love_mapset_count = format( len(df_beatmaps.loc[(df_beatmaps.status=='Love')]),',')
                # 收藏、遊玩數
                favorites_count = format( df_beatmaps.favourite_count.sum(),',')
                platcount_count = format( df_beatmaps.playcount.sum(),',')

                # 最新的圖譜
                New_mapset_id  = str(df_beatmaps.sort_values(by='last_update', ascending=False).head(1).beatmapset_id.values[0])
                New_mapset_artist = df_beatmaps.sort_values(by='last_update', ascending=False).head(1).artist_unicode.values[0]
                New_mapset_title = df_beatmaps.sort_values(by='last_update', ascending=False).head(1).title_unicode.values[0]


                # 卡片
                embed = discord.Embed(title=mapper_name, url='https://osu.ppy.sh/users/'+mapper_id, color=0xff85bc)

                embed.set_thumbnail(url="https://s.ppy.sh/a/"+mapper_id)

                embed.add_field(name="Mapping Age ",value=mapping_age, inline=False)
                embed.add_field(name="Beatmap Count ",value='✍'+mapset_count+'  ✅'+rank_mapset_count+'  ❤'+love_mapset_count, inline=True)
                embed.add_field(name="Playcount & Favorites ",value='▶'+platcount_count+'  💖'+favorites_count, inline=True)
                embed.add_field(name="New Mapset!  "+New_mapset_artist+" - "+New_mapset_title, value='https://osu.ppy.sh/beatmapsets/'+New_mapset_id ,inline=False)

                embed.set_footer(text=date.today().strftime("%Y/%m/%d"))
                await message.channel.send(embed=embed)
        except:
            await message.channel.send('我找不到這位神麻婆的圖;w;')
            
            
    ######################################################## 輸出圖譜 icon bbcode
    if message.content.startswith('icon bbcode '):
        try:
            # 利用osu api取得難度名稱與星級
            beatmap_url = message.content.split("icon bbcode ",1)[1]
            beatmap_id = re.search(r'beatmapsets\/([0-9]*)', beatmap_url).group(1)
            beatmap_meta = requests.get('https://osu.ppy.sh/api/get_beatmaps?k=13a36d70fd32e2f87fd2a7a89e4f52d54ab337a1&s='+beatmap_id).json()
            beatmap_difficulty_list = [meta.get('version') for meta in beatmap_meta]
            beatmap_rating_list = [float(meta.get('difficultyrating')) for meta in beatmap_meta]
            df_beatmap = pd.DataFrame([beatmap_difficulty_list,beatmap_rating_list]).T.rename(columns={0:'difficulty', 1:'rating'}).sort_values(by='rating', ascending=True)

            print_str = ''
            for index, row in df_beatmap.iterrows():
                diff_rating = round(row['rating'],1)
                diff_bbcode = '[img]https://raw.githubusercontent.com/Azuelle/osuStuff/master/diffs/gradient/difficon_std_'+get_rating_color(diff_rating)[1]+'%4016-gap.png[/img] [color='+get_rating_color(diff_rating)[0]+'][b]'+row['difficulty']+'[/b][/color]\n'
                if len(print_str+diff_bbcode)>1990:  # 輸出上限2000字
                    await message.channel.send(print_str)
                    print_str = ''
                print_str = print_str+diff_bbcode
            await message.channel.send(print_str)
        except:
            await message.channel.send('我找不到這張圖;w;')
            
            
    ################################################################ 隨機喊婆
    if message.content.startswith('全婆俠 '):
        
        AniList_userName = message.content.split("全婆俠 ",1)[1]

        # 取得 AniList
        query = '''
        query ($userName: String, $MediaListStatus: MediaListStatus, $page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {hasNextPage}
                mediaList (userName: $userName, status: $MediaListStatus) {
                    media {title{romaji english native}
                           characters{nodes{name{full native} gender image{medium}}}
                      }
                }
            }
        }
        '''
        page_number = 1
        next_page = True

        character_list = []
        character_image_list = []
        character_gender_list = []

        while next_page is True:
            variables = {'userName': AniList_userName, 'MediaListStatus': 'COMPLETED', 'page': page_number, 'perPage': 50 }
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()
            next_page = response.get('data').get('Page').get('pageInfo').get('hasNextPage')

            for anime in response.get('data').get('Page').get('mediaList'):
                #romaji_title = anime.get('media').get('title').get('romaji')
                #english_title = anime.get('media').get('title').get('english')
                #native_title = anime.get('media').get('title').get('native')
                characters = anime.get('media').get('characters').get('nodes')

                for character in characters:
                    #character_name = character.get('name').get('full')
                    character_native = character.get('name').get('native')
                    character_image = character.get('image').get('medium')
                    character_gender = character.get('gender')

                    if (character_native!=None) and (character_image!=None) and (character_gender!=None):
                        character_list.append(character_native)
                        character_image_list.append(character_image)
                        character_gender_list.append(character_gender)
                        
            page_number += 1
            #if page_number>=3:
            #    break


        random_character = list(zip(character_list, character_gender_list, character_image_list))[random.randint(0,len(character_list))]

        if random_character[1] == 'Male':
            wifu_gender = '老公'
        else:
            wifu_gender = '婆'
            
            
        embed=discord.Embed(title=AniList_userName+': '+random_character[0]+'我'+wifu_gender, color=0x7875ff)
        embed.set_image(url=random_character[2])
        await message.channel.send(embed=embed)
        
        
    
    ################################################################ 取得 AniList 其中一首歌曲
    if message.content.startswith('AMQ '):
        
        AniList_userName = message.content.split("AMQ ",1)[1]

        query = '''
        query ($userName: String, $MediaListStatus: MediaListStatus, $page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {hasNextPage}
                mediaList (userName: $userName, status: $MediaListStatus) {
                    media {title{romaji english native}
                      }
                }
            }
        }
        '''
        # COMPLETED
        page_number = 1
        all_anime_list = []
        next_page = True
        while next_page is True:
            variables = {'userName': AniList_userName, 'MediaListStatus': 'COMPLETED', 'page': page_number, 'perPage': 50 }
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()
            next_page = response.get('data').get('Page').get('pageInfo').get('hasNextPage')
            page_number += 1

            anime_list = []
            for anime in response.get('data').get('Page').get('mediaList'):
                romaji_title = anime.get('media').get('title').get('romaji')
                english_title = anime.get('media').get('title').get('english')
                if romaji_title:
                    anime_list.append([romaji_title,english_title])
            all_anime_list = all_anime_list+anime_list
            
        # WATCHING
        page_number = 1
        next_page = True
        while next_page is True:
            variables = {'userName': AniList_userName, 'MediaListStatus': 'CURRENT', 'page': page_number, 'perPage': 50 }
            response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables}).json()
            next_page = response.get('data').get('Page').get('pageInfo').get('hasNextPage')
            page_number += 1

            anime_list = []
            for anime in response.get('data').get('Page').get('mediaList'):
                romaji_title = anime.get('media').get('title').get('romaji')
                english_title = anime.get('media').get('title').get('english')
                if romaji_title:
                    anime_list.append([romaji_title,english_title])
            all_anime_list = all_anime_list+anime_list


        while True:
            try:
                saerch_name = random.choice(all_anime_list)

                animethemes = requests.get('http://animethemes-api.herokuapp.com/api/v1/search/'+saerch_name[0]).json()
                if len(animethemes.get('anime'))==0:
                    animethemes = requests.get('http://animethemes-api.herokuapp.com/api/v1/search/'+saerch_name[1]).json()
                
                ######## 科南回歸用:
                if 'Meitantei Conan' in saerch_name[0]:
                    animethemes = requests.get('http://animethemes-api.herokuapp.com/api/v1/search/Meitantei Conan').json()
                    saerch_name = ['Meitantei Conan','Detective Conan']
                # Another排錯:
                if saerch_name[1] == 'Another':
                    continue
                ########
                
                anime_num = random.randint(0,len(animethemes.get('anime'))-1)
                animetheme_num = random.randint(0,len(animethemes.get('anime')[anime_num].get('themes'))-1)

                theme_type = animethemes.get('anime')[anime_num].get('themes')[animetheme_num].get('type')
                theme_title = animethemes.get('anime')[anime_num].get('themes')[animetheme_num].get('title')
                theme_url = animethemes.get('anime')[anime_num].get('themes')[animetheme_num].get('mirrors')[0].get('mirror')

                await message.channel.send('**'+saerch_name[1]+'** '+theme_type+':  '+theme_title+'\n'+theme_url)
                break

            except:
                #print(saerch_name)
                pass

token = os.environ.get('BOT_TOKEN')
client.run(token)