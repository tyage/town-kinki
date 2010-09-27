sub get_unit {
($sec,$min,$hour,$day,$mon,$year,$week)=localtime(time);
$mon+=1;
if($mon==12){$season="winter";}
elsif($mon>=10){$season="fall";}
elsif($mon>=6){$season="summer";}
elsif($mon>=3){$season="spring";}
elsif($mon>=1){$season="winter";}

if($season eq 'winter'){$tree="<td><img src=$img_dir/winter/x-mas_tree.gif></td>";}
elsif($season eq 'spring'){$tree="<td><img src=$img_dir/spring/sakura.gif></td>";}
elsif($season eq 'summer'){$tree="<td><img src=$img_dir/summer/himawari.gif></td>";}
elsif($season eq 'fall'){$tree="<td><img src=$img_dir/fall/otiba.gif></td>";}
elsif($season eq 'winter'){$tree="<td><img src=$img_dir/winter/x-mas_tree.gif></td>";}

if($mon==1){$tool1="<td><img src=$img_dir/winter/shishimai.gif></td>\n";}
elsif($mon==2){$tool1="<td><img src=$img_dir/winter/oni_blue.gif></td>";}
elsif($season eq 'spring'){$tool1="<td><img src=$img_dir/koinobori.gif></td>";}
elsif($season eq 'summer'){$tool1="<td><img src=$img_dir/iruka.gif></td>";}
elsif($season eq 'winter'){$tool1="<td><img src=$img_dir/x-mas_tree.gif></td>";}


if($mon==1){$tool2="<td><img src=$img_dir/winter/kadomatu.gif></td>\n"}
elsif($mon==2){$tool2="<td><img src=$img_dir/winter/mamemaki.gif></td>";}
elsif($season eq 'spring'){$tool2="<td><img src=$img_dir/koinobori.gif></td>";}
elsif($season eq 'summer'){$tool2="<td><img src=$img_dir/iruka.gif></td>";}
elsif($season eq 'winter'){$tool2="<td><img src=$img_dir/x-mas_tree.gif></td>";}

if($mon==1){$tool3="<td><img src=$img_dir/winter/kite.gif></td>\n"}
elsif($mon==2){$tool3="<td><img src=$img_dir/winter/oni_red.gif></td>";}
elsif($season eq 'spring'){$tool3="<td><img src=$img_dir/koinobori.gif></td>";}
elsif($season eq 'summer'){$tool3="<td><img src=$img_dir/iruka.gif></td>";}
elsif($season eq 'winter'){$tool3="<td><img src=$img_dir/x-mas_tree.gif></td>";}

if($mon==1){$tool4="<td><img src=$img_dir/winter/motituki.gif></td>\n"}
elsif($mon==2){$tool4="<td><img src=$img_dir/winter/namahage.gif></td>";}
elsif($season eq 'spring'){$tool4="<td><img src=$img_dir/koinobori.gif></td>";}
elsif($season eq 'summer'){$tool4="<td><img src=$img_dir/iruka.gif></td>";}
elsif($season eq 'winter'){$tool4="<td><img src=$img_dir/x-mas_tree.gif></td>";}

if($mon==1){$tool5="<td><img src=$img_dir/winter/hagoita.gif></td>\n"}
elsif($mon==2){$tool5="<td><img src=$img_dir/winter/namahage_2.gif></td>";}
elsif($season eq 'spring'){$tool5="<td><img src=$img_dir/koinobori.gif></td>";}
elsif($season eq 'summer'){$tool5="<td><img src=$img_dir/iruka.gif></td>";}
elsif($season eq 'winter'){$tool5="<td><img src=$img_dir/x-mas_tree.gif></td>";}

	if(!$k_id && $in{'name'}){
		open(IN,"< $logfile") || &error("Open Error : $logfile");
		eval{ flock (IN, 1); }; 
		@all_member = <IN>;
		close(IN);
		foreach (@all_member){
			(@kojin_dat) = split(/<>/);
			if ($in{'name'} eq $kojin_dat[1]){
				$k_id = $kojin_dat[0];
				$in{'k_id'} = $k_id;
				last;
			}
		}
	}
	
	%unit = (
"プレ３" => "<form method=POST action=\"test.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>main<>\"><td height=32 width=32><input type=image src='$img_dir/gift.gif' onMouseOver=\"Navi('$img_dir/gift.gif', 'お年玉', 'お年玉もらえるかも', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"プレ２" => "<form method=POST action=\"prezent2.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>top<>\"><td height=32 width=32><input type=image src='$img_dir/gift.gif' onMouseOver=\"Navi('$img_dir/gift.gif', 'プレゼント', 'プレゼントもらえるかも', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"ＰＨＰ" => "<form method=POST action=\"bbs.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>top<>\"><td height=32 width=32><input type=image src='$img_dir/munk.png' onMouseOver=\"Navi('$img_dir/munk.png', 'ＰＨＰver開発用掲示板', 'ＰＨＰver開発用の掲示板です。<br>開発メンバーにはここで入れます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"仕事工場" => "<form method=POST action=\"job.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>top<>\"><td height=32 width=32><input type=image src='$img_dir/idea.gif' onMouseOver=\"Navi('$img_dir/job.gif', 'モンスター投稿', 'Ｂリーグにでてくるモンスターのアイデアを投稿できます。<br>採用されるかもしれません。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"モ投稿" => "<form method=POST action=\"mon_make.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>mon_make<>\"><td height=32 width=32><input type=image src='$img_dir/idea.gif' onMouseOver=\"Navi('$img_dir/idea.gif', 'モンスター投稿', 'Ｂリーグにでてくるモンスターのアイデアを投稿できます。<br>採用されるかもしれません。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"Ｂリーグ" => "<form method=POST action=\"battle.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>bbin<>\"><td height=32 width=32><input type=image src='$img_dir/mon.gif' onMouseOver=\"Navi('$img_dir/mon.gif', 'Ｂリーグ', 'Ｂリーグ会場です。<br>モンスターと頭脳、身体パワーで戦います。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"ランキン" => "<form method=POST action=\"$script\" target=\"_blank\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>jamp_url<>\"><td height=32 width=32><input type=image src='$img_dir/ranking.gif' onMouseOver=\"Navi('$img_dir/ranking.gif', 'ランキング', 'ランキングに投票します。<br>お金がもらえます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"釣り" => "<form method=POST action=\"sea.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>sea<>\"><td height=32 width=32><input type=image src='$img_dir/blank.gif' onMouseOver=\"Navi('$img_dir/umi.gif', '釣り', '釣りができます。<br>釣った魚を売ることもできます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"イベント" => "<form method=POST action=\"event.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>form<>\"><td height=32 width=32><input type=image src='$img_dir/event.gif' onMouseOver=\"Navi('$img_dir/event.gif', 'イベント', 'イベント投稿所です。<br>投稿したイベントが採用されるかもしれません！', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"特典" => "<form method=POST action=\"tokuten.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>tokuten<>\"><td height=32 width=32><input type=image src='$img_dir/kagamimoti.gif' onMouseOver=\"Navi('$img_dir/kagamimoti.gif', '特典', 'なんかイベントあるかもしれません。<br>合言葉が必要です。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"アンケ" => "<form method=POST action=\"enq.cgi\"><input type=hidden name=enq_id value=\"$k_id\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>top<>\"><td height=32 width=32><input type=image src='$img_dir/enq.gif' onMouseOver=\"Navi('$img_dir/enq.gif', 'アンケート', 'アンケートの投稿＆作成ができます。<br>アンケートに答えるとお金がもらえます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"駅" => "<form method=POST action=\"station.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>map<>\"><td height=32 width=32><input type=image src='$img_dir/train.gif' onMouseOver=\"Navi('$img_dir/train.gif', '駅', '他の街に移動できます。<br>ＭＡＰも見れます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"木" => "$tree",
"物１" => "$tool1",
"物２" => "$tool2",
"物３" => "$tool3",
"物４" => "$tool4",
"物５" => "$tool5",
"道１" => "<td><img src=$img_dir/road/1.gif></td>",
"道２" => "<td><img src=$img_dir/road/2.gif></td>",
"道３" => "<td><img src=$img_dir/road/3.gif></td>",
"道４" => "<td><img src=$img_dir/road/4.gif></td>",
"道５" => "<td><img src=$img_dir/road/5.gif></td>",
"道６" => "<td><img src=$img_dir/road/6.gif></td>",
"道７" => "<td><img src=$img_dir/road/7.gif></td>",
"道８" => "<td><img src=$img_dir/road/8.gif></td>",
"道９" => "<td><img src=$img_dir/road/9.gif></td>",
"道横" => "<td><img src=$img_dir/road/yoko.gif></td>",
"道縦" => "<td><img src=$img_dir/road/tate.gif></td>",
"歩道横" => "<td><img src=$img_dir/road/hodo_yoko.gif></td>",
"歩道縦" => "<td><img src=$img_dir/road/hodo_tate.gif></td>",
"信号" => "<td><img src=$img_dir/road/singou.gif width=\"32\" height=\"32\"></td>",
"大仏" => "<td><img src=$img_dir/daibutu.gif></td>",
"鹿" => "<td><img src=$img_dir/sika.gif></td>",
"イルカ" => "<td><img src=$img_dir/iruka.gif></td>",
"みかん" => "<td><img src=$img_dir/mikan.gif width=\"32\" height=\"32\"></td>",
"海" => "<td><img src=$img_dir/umi.gif></td>",
"草" => "<td><img src=$img_dir/kusa.gif></td>",
"砂漠" => "<td><img src=$img_dir/sabaku.gif></td>",
"灯台" => "<td><img src=$img_dir/toudai.gif></td>",

"おばちゃん" => "<form method=POST action=\"obatyan.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>week<>\"><td height=32 width=32><input type=image src='$img_dir/obatyan.gif' onMouseOver=\"Navi('$img_dir/obatyan.gif', '大阪のおばちゃん', '弱いおばちゃんに挑戦状を突きつけます。<br>弱い（？）大阪のおばちゃんと戦います。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"おばちゃん強" => "<form method=POST action=\"obatyan.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>strong<>\"><td height=32 width=32><input type=image src='$img_dir/obatyan2.gif'  onMouseOver=\"Navi('$img_dir/obatyan2.gif', '大阪のおばちゃん', '強いおばちゃんに挑戦状を突きつけます。<br>強い（？）大阪のおばちゃんと戦います。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"ゲーセン" => "<form method=POST action=\"gamerand.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<><>\"><td height=32 width=32><input type=image src='$img_dir/game.gif' onMouseOver=\"Navi('$img_dir/game.gif', 'ゲームランド', 'ゲームランドで遊びます。<br>いろいろなゲームがあります。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"アイテム" => "<form method=POST action=\"item.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>item_make<>\"><td height=32 width=32><input type=image src='$img_dir/idea.gif' onMouseOver=\"Navi('$img_dir/idea.gif', 'アイテム', 'アイテムのアイデア紹介・登録ができます。<br>採用されると実際に商品となります。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"役場" => "<form method=POST action=\"yakuba.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>yakuba<>\"><td height=32 width=32><input type=image src='$img_dir/yakuba.gif' onMouseOver=\"Navi('$img_dir/yakuba.gif', '役場', '役場です。<br>新規に住民登録された方やランキングを見ることができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"銀行" => "<form method=POST action=\"basic.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>ginkou<>\"><td height=32 width=32><input type=image src='$img_dir/bank.gif' onMouseOver=\"Navi('$img_dir/bank.gif', '銀行', '銀行です。<br>お金を預けたり引き出したりできます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"病院" => "<form method=POST action=\"basic.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>byouin<>\"><td height=32 width=32><input type=image src='$img_dir/hospital.gif' onMouseOver=\"Navi('$img_dir/hospital.gif', 'びよういん', '病院です。<br>費用は高めですが、ほとんどの病気を全快させます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"ギフト屋" => "<form method=POST action=\"gifutoya.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>gifutoya<>\"><td height=32 width=32><input type=image src='$img_dir/gift.gif' onMouseOver=\"Navi('$img_dir/gift.gif', 'ギフト作成', 'ギフト作成所です。<br>自分の手持ちのアイテムをギフトにできます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"株" => "<form method=POST action=\"kabu.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>kabu<>\"><td height=32 width=32><input type=image src='$img_dir/kabu.gif' onMouseOver=\"Navi('$img_dir/kabu.gif', '株取引所', '株の取引所です。<br>お金を株に投資することができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"食堂" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>syokudou<>\"><td height=32 width=32><input type=image src='$img_dir/syokudou.gif' onMouseOver=\"Navi('$img_dir/syokudou.gif', '食堂', 'セントラル食堂です。<br>種類は豊富ですが、値段は高めで在庫も少なめです。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"食堂２" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>syokudou2<>\"><td height=32 width=32><input type=image src='$img_dir/syokudou.gif' onMouseOver=\"Navi('$img_dir/syokudou.gif', '食堂', 'セントラル食堂２です。<br>種類は豊富ですが、値段は高めで在庫も少なめです。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"デパ" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>depart_gamen<>\"><td height=32 width=32><input type=image src='$img_dir/depart.gif' onMouseOver=\"Navi('$img_dir/depart.gif', 'デパート', '中央デパートです。<br>種類は豊富ですが、値段は高めで在庫も少なめです。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"デパ2" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>depart_gamen2<>\"><td height=32 width=32><input type=image src='$img_dir/depart.gif' onMouseOver=\"Navi('$img_dir/depart.gif', 'デパート', 'ライバルデパートです。<br>種類は豊富ですが、値段は高めで在庫も少なめです。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"自販機" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>hanbai<>\"><td height=32 width=32><input type=image src='$img_dir/jihanki.gif' onMouseOver=\"Navi('$img_dir/jihanki.gif', 'じはんき', '自動販売機です。<br>飲み物が売ってます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"装備屋" => "<form method=POST action=\"hanbai.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>hanbai<>\"><td height=32 width=32><input type=image src='$img_dir/kaziya.gif' onMouseOver=\"Navi('$img_dir/kaziya.gif', '装備屋', '装備アイテムが売ってます。<br>武器、防具、魔法書、お守りが買えます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"販売1" => "<form method=POST action=\"hanbai1.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>hanbai1<>\"><td height=32 width=32><input type=image src='$img_dir/house/house1.gif' onMouseOver=\"Navi('$img_dir/house/house1.gif', 'お店', 'みんなのお店屋です。<br>魚の餌が売ってます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"リサイ" => "<form method=POST action=\"recycle.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>resycle<>\"><td height=32 width=32><input height=32 width=32 type=image src='$img_dir/resai.gif' onMouseOver=\"Navi('$img_dir/resai.gif', 'リサイクル', 'リサイクルショップです。<br>要らない持ち物を売ったり買うことが出来ます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"クーポン" => "<form method=POST action=\"coupon.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>coupon<>\"><td height=32 width=32><input type=image src='$img_dir/coupon.gif' onMouseOver=\"Navi('$img_dir/coupon.gif', 'クーポン', 'クーポン引換所です。<br>クーポンとアイテムを交換することができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"教室" => "<form method=POST action=\"kyushitu.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>kyushitu<>\"><td height=32 width=32><input type=image src='$img_dir/kyositu.gif' onMouseOver=\"Navi('$img_dir/kyositu.gif', '教室', '教室です。<br>脳と体を鍛えることができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"職安" => "<form method=POST action=\"basic.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>job_change<>\"><td height=32 width=32><input type=image src='$img_dir/work.gif' onMouseOver=\"Navi('$img_dir/work.gif', '職安', '職業安定所です。<br>就職、転職などはこちらへ。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"空地" => "<td><img src=$img_dir/akiti.gif onMouseOver=\"Navi('$img_dir/akiti.gif', '空地', '空地です。<br>この場所に家を建てることができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td>",

"問屋" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>orosi<>\"><td height=32 width=32><input type=image src=\"$img_dir/tonya.gif\" onMouseOver=\"Navi('$img_dir/tonya.gif', '問屋', '問屋です。<br>商店や企業を持っている人は、ここで商品を仕入れることができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"建築" => "<form method=POST action=\"$script\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>kentiku<>\"><td height=32 width=32><input type=image src=\"$img_dir/kentiku.gif\" onMouseOver=\"Navi('$img_dir/kentiku.gif', '建設', '建設会社です。<br>家を建てたいときはここに依頼します。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"競馬" => "<form method=POST action=\"basic.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>keiba<>\"><td height=32 width=32><input type=image src=\"$img_dir/keiba.gif\" onMouseOver=\"Navi('$img_dir/keiba.gif', '競馬', '競馬場です。<br>競馬でお金を稼ぐことができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"プロフ" => "<form method=POST action=\"basic.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>prof<>\"><td height=32 width=32><input type=image src=\"$img_dir/prof.gif\" onMouseOver=\"Navi('$img_dir/prof.gif', 'プロフ', 'プロフです。<br>住民の実際のプロフィールを登録するところです。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"キャラ" => "<form method=POST action=\"game.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>c_league<>\"><td height=32 width=32><input type=image src=\"$img_dir/chara_battle.gif\" onMouseOver=\"Navi('$img_dir/chara_battle.gif', 'Cリーグ', '最強のキャラクターを決める『Cリーグ』会場です。<br>キャラ作成もここでできます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"街コン" => "<form method=POST action=\"./mati_contest.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>matikon<>\"><td height=32 width=32><input type=image src=\"$img_dir/matikon.gif\" onMouseOver=\"Navi('$img_dir/matikon.gif', '街コン', '街の名誉をかけて競う『週間街コンテスト』です。<br>優勝した町の住民には賞金が！', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"地" => "<td><img src=$img_dir/kentiku_yotei.gif onMouseOver=\"Navi('$img_dir/kentiku_yotei.gif', '予\定地', '建築予\定地です。<br>ここに家を建てます。');\"></td>",

"温泉" => "
<script type=\"text/javascript\">
<!--
function on_sec(){
	myonDate = Math.round((new Date()).getTime()/1000);
	document.onsen.onsec.value = myonDate;
}
//-->
</script>
<form method=POST name=onsen action=\"basic.cgi\"><input type=hidden name=onsec value=\"\"><!-- koko 2007/06/11 --><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>onsen<>\"><td height=32 width=32><input type=image src=\"$img_dir/onsen.gif\" onMouseOver=\"Navi('$img_dir/onsen.gif', '温泉', '疲れた体を癒しましょう。<br>入浴料は$nyuuyokuryou円です。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"斡旋" => "<form method=POST action=\"kekkon.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>assenjo<>\"><td height=32 width=32><input type=image src=\"$img_dir/assenjo.gif\" onMouseOver=\"Navi('$img_dir/assenjo.gif', '斡旋所', '恋人斡旋所です。<br>バーチャルな恋愛や結婚をしたい方はこちらへ登録してください。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"人生" => "<form method=POST action=\"./sugoroku/zinsei.cgi\"><input type=hidden name=name value=$in{'name'}><input type=hidden name=pass value=$in{'pass'}><input type=hidden name=sex value=$sex><input type=hidden name=mode value=cont><input type=hidden name=yobidasi value=login_view><input type=hidden name=command value=select_com><td height=32 width=32><input type=hidden name=town_no value=$in{'town_no'}><input type=image src=\"$img_dir/zinsei.gif\" onMouseOver=\"Navi('$img_dir/zinsei.gif', '人生のゲーム', '「人生のゲーム」です。<br>稼いだお金をTOWNの銀行に振り込むことができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"合成" => "<form method=POST action=\"gouseiya.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>gousei<>\"><td height=32 width=32><input type=image src='$img_dir/gouseiyai.gif' onMouseOver=\"Navi('$img_dir/gouseiyai.gif', '合成', '合成所です。<br>商品を合成して新しい商品を作ります。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

"競売" => "<form method=POST action=\"auction.cgi\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>auction<>\"><td height=32 width=32><input type=image src='$img_dir/auction.gif' onMouseOver=\"Navi('$img_dir/auction.gif', '競売', '競売所です。<br>オークションに出品、落札ができます。', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>",

);

}

sub kozin_house {
	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (OI, 2); };
	@ori_ie_hairetu = <OI>;
	foreach (@ori_ie_hairetu) {
		&ori_ie_sprit($_);
		if($ori_ie_rank==1){
			$ie_syubetu="運営会社";
		}elsif($ori_ie_rank==2){
			$ie_syubetu="株式会社";
		}elsif($ori_ie_rank==3){
			$ie_syubetu="持ち物販売店";
		}else{
			if($ori_ie_syubetu){
				$ie_syubetu="家（$ori_ie_syubetu）";
			}elsif($ori_k_id=~/_/){
				$ie_syubetu="家（支部）";
			}else{
				$ie_syubetu="家（店なし）";
			}
		}
		$ori_ie_image =~ s/'/%/g;
		$ori_ie_image =~ s/<>/&lt;&gt;/g;
		$ori_ie_setumei =~ s/<>/&lt;&gt;/g;
		$ori_ie_setumei =~ s/<>/&lt;&gt;/g;
		$unit{"$ori_k_id"} = "<form method=POST action=\"original_house.cgi\"><input type=hidden name=ori_ie_id value=\"$ori_k_id\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>houmon<>\"><td height=32 width=32><input type=image src=\"$ori_ie_image\" onMouseOver=\"Navi('$ori_ie_image', '『$ori_ie_name』の$ie_syubetu', '$ori_ie_setumei', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>";
	}
	close(OI);
}

sub simaitosi {
	$i=0;
	$i2=1;
	foreach (@town_hairetu) {
			$unit{"街$i2"} = "<form method=POST action=\"$script\"><input type=hidden name=command value=\"mati_idou\"><input type=hidden name=maemati value=\"$in{'town_no'}\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$i<>login_view<>\"><td height=32 width=32><input type=image src=\"$img_dir/mati_link.gif\" onMouseOver=\"Navi('$img_dir/mati_link.gif', '移動', '移動します。<br>$_へ移動', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>";
			$i ++;
			$i2 ++;
	}
}

sub simaitosi2 {
	$i=0;
	$i2=1;
	foreach (@town_hairetu) {
			$unit{"バス$i2"} = "<form method=POST action=\"$script\"><input type=hidden name=command value=\"mati_idou2\"><input type=hidden name=maemati value=\"$in{'town_no'}\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$i<>login_view<>\"><td height=32 width=32><input type=image src=\"$img_dir/bus.gif\" onMouseOver=\"Navi('$img_dir/bus.gif', '移動', 'バスで移動します。<br>$_へバスで移動', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>";
			$i ++;
			$i2 ++;
	}
}

sub admin_parts {
	$i=1;
	$i2=0;
	foreach (@admin_bbs_syurui) {
			$unit{"掲$i"} = "<form method=POST action=\"original_house.cgi\"><input type=hidden name=ori_ie_id value=\"admin\"><input type=hidden name=bbs_num value=\"$i2\"><input type=\"hidden\" name=\"my_data\" value=\"$name<>$pass<>$k_id<>$in{'town_no'}<>normal_bbs<>\"><td height=32 width=32><input type=image src=\"$img_dir/$admin_bbs_gazou[$i2]\" onMouseOver=\"Navi('$img_dir/$admin_bbs_gazou[$i2]', '掲示板', '掲示板です。<br>$_', 0, event);\" onMouseOut=\"NaviClose();\"></td></form>";
			$i ++;
			$i2 ++;
	}
}

1;