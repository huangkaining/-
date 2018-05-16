function leftlist(userau){
            var div1=document.getElementById("div1");
            var div2=document.getElementById("div2");
            var div3=document.getElementById("div3");
            var div4=document.getElementById("div4");
            var ch1="";
            var ch2="";
            var ch3="";
            var ch4="";
            if (userau == 1){
                ch1+="<li><a href=\"/scorestu\"><span>个人数据</span></a></li>";
				ch1+="<li><a href=\"/prizedeclare\"><span>获奖信息申报</span></a></li>";
                ch2+="<li><a href=\"/consumptionstu\"><span>个人消费分析</span></a></li>";
                ch3+="<li><a href=\"/cleanone\"><span>个人宿舍得分</span></a></li>";
                ch3+="<li><a href=\"/studyone\"><span>个人集体自习</span></a></li>";
				ch4+="<li><a href=\"/clubone\"><span>社团签到统计</span></a></li>";
            }
            else if (userau == 2){
               ch1+="<li><a href=\"/inclass\"><span>班内数据分析</span></a></li>";
               ch2+="<li><a href=\"/classconsumption\"><span>班内消费分析</span></a></li>";
               ch3+="<li><a href=\"/cleanclass\"><span>班内卫生对比</span></a></li>";
               ch3+="<li><a href=\"/studyclass\"><span>班内集体自习</span></a></li>";
			   ch4+="<li><a href=\"/clubenergy\"><span>社团活力分析</span></a></li>";
             }
            else if (userau == 3){
                ch1+="<li><a href=\"/ingrade\"><span>班间数据分析</span></a></li>";
                ch1+="<li><a href=\"/fileimport\"><span>信息导入</span></a></li>";
                ch2+="<li><a href=\"/mealconsumption\"><span>用餐人数走向</span></a></li>";
                ch2+="<li><a href=\"/mealoccupy\"><span>用餐率分析</span></a></li>";
                ch3+="<li><a href=\"/cleanall\"><span>班间卫生对比</span></a></li>";
                ch4+="<li><a href=\"/clubenergy\"><span>社团活力分析</span></a></li>";
                ch2+="<li><a href=\"/poorstudent\"><span>贫困生分析</span></a></li>";
            }
            else if (userau == 4){
                ch1+="<li><a href=\"/scorestu\"><span>个人数据</span></a></li>";
				ch1+="<li><a href=\"/prizedeclare\"><span>获奖信息申报</span></a></li>";
                ch2+="<li><a href=\"/consumptionstu\"><span>个人消费分析</span></a></li>";
                ch3+="<li><a href=\"/cleanone\"><span>个人宿舍得分</span></a></li>";
                ch3+="<li><a href=\"/studyone\"><span>个人集体自习</span></a></li>";
                ch4+="<li><a href=\"/clubpic\"><span>社团签到</span></a></li>";
                ch4+="<li><a href=\"/clubmanage\"><span>社团管理</span></a></li>";
            }
            ch1+="";
            ch2+="";
            ch3+="";
            ch4+="";
            div1.innerHTML=ch1;
            div2.innerHTML=ch2;
            div3.innerHTML=ch3;
            div4.innerHTML=ch4;
        }