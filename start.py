from parse_avito import *
#from parse import *
import io

def go(url, username, password, hookurl, items, pause):
	AvitoParse(url=url,
			   username=username,
			   password=password,
               hookurl=hookurl,
	           items=items, 
	           count=1,
               pause=pause).parse()
	
    

####################################### Настройки ####################################
with io.open('settings.txt', encoding='utf-8') as f:
	s = f.readlines()
	d = {}
	for i in s:
		i = i.partition('=')
		d[i[0]] = i[2].rstrip('\n')
url = []
hookurl = []
i=1
for i in range(1, 11):
    url.append(d[f'url{str(i)}']+'&s=104&user=1')
    hookurl.append((d[f'hookurl{str(i)}']))
username = d['username']        # Логин от Авито
password = d['password']        # Пароль от Авито
#url.append(d['url1'] + '&s=104&user=1')
#url.append(d['url2'] + '&s=104&user=1')
#url.append(d['url3'] + '&s=104&user=1')
#hookurl = d['hookurl']
pause = int(d['pause'])                    # Пауза между обновлениями в секундах
items = []                             # Ключевые слова, которые должны быть в ОПИСАНИИ товара. Если таких нет - оставить скобки пустыми []
print(hookurl)
if __name__ == "__main__":
    url = url# + "#login?authsrc=h"
    #go(url, username, password, hookurl, items, pause)