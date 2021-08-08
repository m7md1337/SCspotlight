# SCspotlight
* A script python to let you upload on spotlight 
## how to use 
* ### there's two options 1 ,2
1. - by login 
2. - by enter the token  

*  [Note] i recommend use option 2 because some time when login even the pass is correct they said "That's not the right password" and now u will lose ur mind


* #### by login 


    * just enter your password and username
    
    * now i think every one know how to use option 1 so lets describe option 2

* #### by enter the token

    * simple steps to get token 
    
    1. first go to https://my.snapchat.com
    
    2. then click button signin and login after login they will redirect you to my.snapchat.com
    
    3. after that's click right and inspect -> console
    
    4. copy two line javascript below and paste it in the console

    5. now copy the token and paste it on script

```javascript
// javascript to get token
N = JSON.parse(sessionStorage["auth"]) ;
N.token;

```





* ### after use option 2 OR 1
* * now the token will save in file called .envspot so when use script again no need to enter th token or login untill the token expires 
* * but all your videos in dir vids 
* * now the script will ask u how many times upload the videos in direction vids







## why


* i made it just for fun and learning 



## something u should know 
* more than 200 lines i wrote it from my iphone 7
* I tried to setup sms login but I don't think its work
* its work with me maybe won't work with you 
* maybe in the future will be more update maybe
* in the end my language not very good so sorry for any mistake
