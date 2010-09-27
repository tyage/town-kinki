#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

$this_script = 'cardw2.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
#条件分岐
	if($in{'mode'} eq "cardw"){&cardw;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub cardw
	{
	#各種設定＠＠
	
	#支払う金額を持ってないと（0引けない、1引ける）
	$cardw_chk=0;
	
	#レート設定
	#レート設定関係はすべて数を合わせてください

	#1レートの金額（円）
	@cardw_r =("10000","100000","1000000","10000000","100000000");
	#1レート表示設定1
	@cardw_h1 =("1","10","100","1000","1");
	#1レート表示設定2
	@cardw_h2 =("万","万","万","万","億");
	#レートごとのあたり確率設定（％）
	@cardw_atari =("80","65","50","35","20");

	#レートごとの時間設定（分）
#	@cardw_k_time =("15","20","25","30","35");
	@cardw_k_time =("0","0","0","0","0");
	
	
	#1レート表示設定1+2が画面に表示されます
	#レート数2の場合
	#1万円コース	2万円必要です	当たり確率：80％  ゲーム間隔：15分  
	#10万円コース	20万円必要です	当たり確率：65％  ゲーム間隔：20分  
	#100万円コース	200万円必要です	当たり確率：50％  ゲーム間隔：25分  
	#1000万円コース	2000万円必要です	当たり確率：35％  ゲーム間隔：30分  
	#1億円コース	2億円必要です	当たり確率：20％  ゲーム間隔：35分  

 
	#レート設定終了＠＠
	
	#ログファイルの設定
	$cardw_logfile='./log_dir/cardw_log2.cgi';
	
	#当たりの画像の場所
	$cardw_a_img="img/renai.gif";
	#ハズレの画像の場所
	$cardw_h_img="img/battle.gif";
	
	open(MA,"$cardw_logfile") || &error("$cardw_logfileが開けません");
	$saigonohito = <MA>;
	@donuts_alldata = <MA>;
	close(MA);
	$sankasyasuu = @donuts_alldata;
	($do_name,$do_hantei,$do_hiitakard,$card_suu,$do_yobi1,$do_last)= split(/<>/,$saigonohito);
#do_yobi1 = 支払額
	$my_card = "";
	if($card_suu eq ""){$card_suu=1;}

	@cardw_hitu1=();
	@cardw_hitu2=();
	
	$cardw_suu=0;
	foreach(@cardw_r)
		{
		if($money>=($_*$card_suu) || $cardw_chk ==1)
			{
			$cardw_hitu1[$cardw_suu]="<input type=radio value=\"$cardw_suu\" name=\"chk\">";
			}
		else
			{
			$cardw_hitu1[$cardw_suu]="×";
			}
		if($cardw_chk ==0)
			{
			$r_hyouji = $cardw_h1[$cardw_suu] * $card_suu;
			$cardw_hitu2[$cardw_suu] ="<TD>$r_hyouji$cardw_h2[$cardw_suu]円必要です";
			}
		$cardw_suu++;
		}
#引くコマンドだった場合
	if ($in{'command'} eq "hiku")
		{
		$now_time = time ;
		if ($name eq $do_name){&error("同じ方が続けてカードを引くことはできません");}		foreach (@donuts_alldata)
			{
			($do2_name,$do2_hantei,$do2_hiitakard,$card_suu2,$do2_yobi1,$do2_last)= split(/<>/);
			if ($name eq $do2_name)
				{
				if ($now_time - $do2_last < 60*$cardw_k_time[$in{'chk'}])
				
				
					{
					&error("最後にゲームしてからまだ$cardw_k_time[$in{'chk'}]分すぎていません。");
					
					}
				}
			}
		if($in{'chk'} eq ""){&error("コースを選択してください$in{'chk'}");}
		$randed = int(rand(100))+1;
		if($cardw_atari[$in{'chk'}] <= $randed)
			{
			$randimg="$cardw_h_img";
			$rande=$randed;
			$randed = "hazure";
			}
		else
			{
			$randimg="$cardw_a_img";
			$rande=$randed;
			$randed = "atari";
			}
		$my_card = "<img src=$randimg>";
		$c_hyouji=$card_suu*$cardw_h1[$in{'chk'}];
		$c_hyouji="$c_hyouji$cardw_h2[$in{'chk'}]円";
#アウトの場合
		
		if ($randed eq "hazure")
			{
			$money -= $cardw_r[$in{'chk'}]*$card_suu;
			$do_hantei = "<div class=mainasu>$nameさんが$cardw_h1[$in{'chk'}]$cardw_h2[$in{'chk'}]円コースに挑戦。$c_hyoujiを支払いました。</div>";
			$comment = "<div class=mainasu>アウトォーー！！<br>$c_hyoujiを支払いました！</div>";
			$card_suu =1;
#セーフの場合
		}else{
				$money += $cardw_r[$in{'chk'}]*$card_suu;
				$do_hantei = "<div class=purasu>$nameさんが$cardw_h1[$in{'chk'}]$cardw_h2[$in{'chk'}]円コースに挑戦。$c_hyoujiを入手しました。</div>";
				$comment = "<div class=purasu>セーフ！！<br>$c_hyoujiをゲットしました！</div>";
				$card_suu++ ;
		}
		$next_temp = "$name<>$do_hantei<>$randed<>$card_suu<>$siharai<>$now_time<>\n";
		unshift @donuts_alldata,$saigonohito;
		unshift @donuts_alldata,$next_temp;
		if ($sankasyasuu >= 19){pop @donuts_alldata;}
#データ更新
		&lock;
	open(KB,">$cardw_logfile")|| &error("Open Error : $cardw_logfile");
	print KB @donuts_alldata;
	close(KB);
		&unlock;
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);		
	}		#引く場合の閉じ
	&header(gym_style);
	if($cardw_chk ==0)
		{$c_mess="所持金が足りない人や、";}
	else{$c_mess="";}
			print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●ルール説明<br>
	・参加者がすることはカードを１枚引くことだけです。<br>・引いたカードがあたりの場合、必要金額のお金がもらえ、レートが+1されます。<br>・ハズレが出てしまった場合、逆に必要金額のお金を支払わなければいけません。またレートは1からスタートとなります。<br>※$c_mess同じ人が続けてカードを引くことはできません。</td>
	<td  bgcolor=#333333 align=center width=35%><img src="$img_dir/donuts_tytle.gif"></td>
	</tr></table><br>
	<table width="90%" border="0" cellspacing="2" cellpadding="8" align=center class=yosumi><tr><td>
	<div align=center>
	$my_card
	$comment
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="cardw">
	<input type=hidden name=command value="hiku">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value=$in{'town_no'}>
	$nameさんの所持金：$money円
	<BR><BR>現在のレートは$card_suuです
	<table border="1"align=center class=yosumi>
EOM
	$r_hyou=0;
	foreach(@cardw_r)
		{
		print <<"EOM";
		<TR><TD align=center>$cardw_hitu1[$r_hyou]
		<TD>$cardw_h1[$r_hyou]$cardw_h2[$r_hyou]円コース
		$cardw_hitu2[$r_hyou]
		<TD>当たり確率：$cardw_atari[$r_hyou]％
		<TD>ゲーム間隔：$cardw_k_time[$r_hyou]分
EOM
		$r_hyou++;
		}
	print <<"EOM";
	</table>
	<BR>
<input type=hidden name=gamerand value="$in{'gamerand'}">
	<input type=submit value="カードを引く">
	</form>
EOM

	for ($i=0; $i < $card_suu; $i ++){
		$card_bangou = substr ($do_narandacard,$i,1);
		$table_card_image = "$img_dir/donuts/$card_bangou". ".gif";
			$line .= "<img src=$table_card_image width=30 height=40>\n";

	}

	print <<"EOM";
	</div></td></table>
	</td></tr></table>
	
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
	<div class=honbun2>■最近のゲーム</div>
EOM
	if ($in{'command'} eq ""){
		unshift @donuts_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@donuts_alldata)
			{
			($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/);
				print "$do_hantei";

		}
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
	}
