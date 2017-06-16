
var rmenu = [
									
["長森宏恭",
	"/exhibition/019/",
"長森宏恭 写真展「舞妓とし純　二十歳の君へ」",
""
],
									
["吉田晴美",
"/exhibition/006/",
"織・キルト・器 コラボ<br />創作キルト～ジャワ更紗の世界を創作で紡ぐ～"
],
									
["浅井泰雄",
	"/exhibition/009/",
"油絵 ～ＪＡＺＺを描く～"
],
									
["服部恵一",
	"/exhibition/018/",
"服部恵一博覧会 ～探鳥・潜水・人生～ BIRDS! DIVE! LIFE",
""
],
									
["高田嘉宏",
	"/exhibition/017/",
"日本画個展<br />～乱舞～ 集う・・",
""
],
									
["俊英よんまる会",
	"/exhibition/016/",
"水彩と造形展"
],
									
["山田祥照",
	"/exhibition/015/",
"～回想・西国三十三ヵ所～"
],
									
["豊原香代子",
	"/exhibition/014/",
"～第42回展～<br />布ーいのちの輝き"
],
									
["アールグレイの会",
	"/exhibition/012/",
"（東京セッション）"
],
									
["岡山正春・ＯＫ",
	"/exhibition/011/",
"アート木工２人作品<br />～流木・自然木の雑貨～"
],
									
["野口藍・齋藤さつき",
	"/exhibition/010/",
"なみまにさんかく<br />～ありすｉｎ和ンダーラント～"
],
									
["かめだようこ",
"/exhibition/007/",
"織・キルト・器 コラボ<br />普段着の京・陶器"
],
									
["小山恵市",
"/exhibition/005/",
"野鳥写真<br />～鳥・いま まさに～"
],
									
["城研三",
"/exhibition/004/",
"カシミアでマフラー織り<br />～さをりの森 in 宮川町～"
],
									
["宅島澪",
"/exhibition/003/",
"2人作品<br />fashion ～Sleepy eye's girl～"
],
									
["井上佳澄",
"/exhibition/003-2/",
"2人作品<br />illustration ～Sleepy eye's girl～"
],
									
["阿部元子",
"/exhibition/002/",
"編み物<br />～糸で意図を表現～"
],
									
["山下康一",
"/exhibition/001/",
"水彩画<br />～信州・安曇野の風景～"
]//最後はカンマなし
									
]

var recent_num = 3;

function rmenus_recent(){
	rmenus(recent_num);
}


function rmenus(recent){
	var rm_header;
	recent ? rm_header = '<h2><img src="/common_images/h_side02.gif" alt="最近の展示の様子" width="180" height="28" /></h2>'
	       : rm_header = '<h2><img src="/common_images/h_side01.gif" alt="アーカイブス" width="180" height="28" /></h2>';
	var rm_start = rm_header + '<div class="menu"><ul class="unordered03">';
	var rm_end = '</ul></div>';
	var new_icon;
	var end_sign;
	document.write(rm_start);
	
	for(i=0; i<rmenu.length; i++){
		
		rmenu[i][3] == 'new' ? new_icon = ' new' : new_icon = '';
		i == rmenu.length - 1 ? end_sign = ' class="end"' : end_sign = '';
		
		if(recent){
				if(i < recent_num){
					if(i == recent_num -1)  end_sign = ' class="end"';
					document.write('<li' + end_sign +'><a href="'+rmenu[i][1]+'"><strong class="name' + new_icon + '">'+rmenu[i][0]+'</strong><br />'+rmenu[i][2]+'</a></li>');
					continue;
				}else{
					break;
				}
		}else{
			document.write('<li' + end_sign +'><a href="'+rmenu[i][1]+'"><strong class="name' + new_icon + '">'+rmenu[i][0]+'</strong><br />'+rmenu[i][2]+'</a></li>');
		}
	}
	document.write(rm_end);
}

//バナー

var rbnr_head = '			<ul class="banner">';
var rbnr_foot = '</ul>';

var rbnr_top = '<li><a href="https://www.airbnb.jp/rooms/7958453?s=sNEPn7My" target="_blank"><img src="/common_images/bnr_yamagoya.png" width="180" height="113" alt="8 BED HAKUBA LODGE" /></a></li><li><a href="http://rakuza.gh-project.com/" target="_blank"><img src="/common_images/bnr_rakuza.jpg" width="180" height="113" alt="100年の歴史を持つ元お茶屋を改装された、京都町家（町屋）ゲストハウス「楽座」" /></a></li>';
rbnr_top += '<li><a href="http://agaru168.jp/" target="_blank"><img src="/common_images/bnr_noboru.jpg" width="180" height="113" alt="高瀬川のせせらぎと川沿いの桜並木、京都 宿「西木屋町 仏光寺上る」" /></a></li>';
rbnr_top += '<li><a href="/history/"><img src="/common_images/bnr_miyagawa.jpg" width="180" height="113" alt="宮川町の歴史" /></a></li>';

var rbnr = '';

rbnr_top = rbnr_head + rbnr_top + rbnr_foot;
rbnr = rbnr_head + rbnr + rbnr_foot;

function rbanner_top() {
	document.write(rbnr_top);
}

function rbanner() {
	document.write(rbnr);
}

//宮川町の歴史

function rmenus_history(){
	var rmenu_his = [];
 rmenu_his = [
									
["宮川町の歴史 その1",
	"/history/"
],
									
["宮川町の歴史 その2",
	"/history/no2.html"
]

];
	var rm_header = '<h2><img src="/common_images/h_side01.gif" alt="アーカイブス" width="180" height="28" /></h2>';
	var rm_start = rm_header + '<div class="menu"><ul class="unordered03">';
	var rm_end = '</ul></div>';
	var end_sign;
	
	document.write(rm_start);
	for(i=0; i<rmenu_his.length; i++){
		i == rmenu_his.length -1 ? end_sign = ' class="end"' : end_sign = '';
		document.write('<li' + end_sign + '><a href="' + rmenu_his[i][1] + '">' + rmenu_his[i][0] + '</a></li>');
	}
	document.write(rm_end);
}

