#!/usr/bin/perl

################################
#ドーナツゲームログファイル
$donuts_logfile='./log_dir/donutslog.cgi';
#ドーナツゲームログファイル2
$donuts2_logfile='./log_dir/donutslog2.cgi';
#ドーナツゲームログファイル3
$donuts3_logfile='./log_dir/donutslog3.cgi';
#ドーナツゲームH&Lログファイル4
$donuts4_logfile='./log_dir/donutslog4.cgi';

#ドーナツゲーム掛け金
$donuts_kakekin = "10000";
#ドーナツゲーム掛け金2
$donuts_kakekin2 = "20000";
#ドーナツゲーム掛け金3
$donuts_kakekin3 = "100000";
#ドーナツゲーム掛け金4
$donuts_kakekin4 = "10000";

# H&Lの同じ時 #koko 2005/05/05 'アウト','セーフ'
$dorou = 'セーフ';
# 同じカードの時の倍率 0=支払い無し 1=普通と同じ 2=倍になる
$doroubai = 2;
################################

$this_script = 'donut.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;

#==========メンテチェック==========#
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}

#==========制限時間チェック==========#
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#==========条件分岐==========#
if($in{'mode'} eq "donus"){&donus;}
elsif($in{'mode'} eq "donus2"){&donus2;}
elsif($in{'mode'} eq "donus3"){&donus3;}
elsif($in{'mode'} eq "donus4"){&donus4;}
else{&error("「戻る」ボタンで街に戻ってください");}
	
exit;
	
####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

####ドーナツゲーム
sub donus {
	if ($tajuukinsi_flag==1){&tajuucheck;}
	open(MA,"< $donuts_logfile") || &error("$donuts_logfileが開けません");
	eval{ flock (MA, 1); };
	$saigonohito = <MA>;
	@donuts_alldata = <MA>;
	close(MA);
	$sankasyasuu = @donuts_alldata;
	($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/,$saigonohito);
#do_yobi1 = 支払額
	if ($do_narandacard eq ""){$do_narandacard = 1;}
	$card_suu = length $do_narandacard;
	$my_card = "<img src=$img_dir/donuts/ura.gif width=64 heith=84>";
#引くコマンドだった場合
#koko2008/04/30
	if($renzokuhiki eq 'yes'){$hiku_kaisuu = 3;}else{$hiku_kaisuu = 1;}
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if($renzokuhiki eq 'yes'){
			(@tim_hiniti) = localtime($now_time);
			(@tim_hiniti_mae) = localtime($do_last);
			if ($name eq $do_name && $tim_hiniti[3] == $tim_hiniti_mae[3]){
				($do_name0,$do_hantei0,$do_hiitakard0,$do_narandacard0,$do_yobi10,$do_last0)= split(/<>/,$donuts_alldata[0]);
				(@tim_hiniti_mae) = localtime($do_last0);
				if ($name eq $do_name0 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
					($do_name1,$do_hantei1,$do_hiitakard1,$do_narandacard1,$do_yobi11,$do_last1)= split(/<>/,$donuts_alldata[1]);
					(@tim_hiniti_mae) = localtime($do_last1);
					if ($name eq $do_name1 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
						&error("同じ日に同じ方が続けてカードを引けるのは３回までです。");
					}
				}
			}
		}else{
			if ($name eq $do_name){&error("同じ方が続けてカードを引くことはできません");}
		}
#end2008/04/30
		foreach (@donuts_alldata){
			($do2_name,$do2_hantei,$do2_hiitakard,$do2_narandacard,$do2_yobi1,$do2_last)= split(/<>/);
			if ($name eq $do2_name){
		#		if ($now_time - $do2_last < 60*$crad_game_time){&error("最後にゲームしてからまだ$crad_game_time分すぎていません。");}
			}
		}
		$randed= int(rand(5))+1;
		$my_card_gazou = "$img_dir/donuts/"."$randed"."a.gif";
		$my_card = "<img src=$my_card_gazou width=64 heith=84>";
		$kingaku = $card_suu * 10000;
#アウトの場合
		if ($randed == $do_hiitakard){
			$money -= $kingaku * 1;
			$do_hantei = "out";
			$do_narandacard = "$randed";
			$out_gaku = $card_suu*1;
			$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
			$siharai= $card_suu * 1;
			$card_suu = 1;
#セーフの場合
		}else{
			$money += $kingaku;
			$do_hantei = "safe";
			$do_narandacard = "$do_narandacard" . "$randed";
			$comment = "<div class=purasu>セーフ！！<br>$card_suu万円をゲットしました！</div>";
			$siharai= $card_suu;
		}
		$next_temp = "$name<>$do_hantei<>$randed<>$do_narandacard<>$siharai<>$now_time<>\n";
		unshift @donuts_alldata,$saigonohito;
		unshift @donuts_alldata,$next_temp;
		if ($sankasyasuu >= 19){pop @donuts_alldata;}
#データ更新
		&lock;
		open(KB,">$donuts_logfile")|| &error("Open Error : $donuts_logfile");
		eval{ flock (KB, 2); };
		print KB @donuts_alldata;
		close(KB);
		&unlock;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);		
	}		#引く場合の閉じ
	&header(gym_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●ルール説明<br>
・参加者がすることはカードを１枚引くことだけです。<br>・引いたカードが前の人のカードと違っていれば、その時点でテーブルにたまっているカードの数×１万円のお金がもらえ、またそのカードがテーブルにたまっていきます。<br>・同じ数が出てしまった場合、逆にカードの数×１万円のお金を支払わなければいけません。またテーブルのカードは１枚からスタートとなります。<br>※同じ人が同じ日に続けてカードを$hiku_kaisuu回引くことが出来ます。※ゲーム間隔は$crad_game_time分です。</td>
<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>カードゲーム</b></font></td>
</tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
<div align=center>
$my_card
$comment
<form method="POST" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="donus">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="カードを引く">
</form></div>
EOM

	if ($do_hiitakard ne ""){
		$your_card = "$img_dir/donuts/$do_hiitakard" .".gif";
		print <<"EOM";
<div align=center><img src=$your_card width=60 heith=80></div>
<div align=center>前の人が引いたカード</div>
EOM
	}

	for ($i=0; $i < $card_suu; $i ++){
		$card_bangou = substr ($do_narandacard,$i,1);
		$table_card_image = "$img_dir/donuts/$card_bangou". ".gif";
		$line .= "<img src=$table_card_image width=30 height=40>\n";
	}

	print <<"EOM";
</td><td width=60% valign=top>
<div class=job_messe>＜現在までの引かれたカード＞</div>
<table  border="0" cellspacing="0" cellpadding="10" width=100% height=80% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
<tr><td>
$line
</td></tr></table>
</td></tr></table>
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>
<div class=honbun2>■最近のゲーム</div>
EOM
	if ($in{'command'} eq ""){
		unshift @donuts_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@donuts_alldata){
			($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/);
			$ikura = length $do_narandacard;
			if ($do_hantei eq "out"){
				print "<div class=mainasu>$do_nameさんが$do_yobi1万円を支払いました。</div>";
			}else{
				print "<div class=purasu>$do_nameさんが$do_yobi1万円をゲットしました。</div>";
			}
		}
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
}
####ドーナツゲーム２
sub donus2 {
	if ($tajuukinsi_flag==1){&tajuucheck;}
	open(MA,"< $donuts2_logfile") || &error("$donuts2_logfileが開けません");
	eval{ flock (MA, 1); };
	$saigonohito = <MA>;
	@donuts_alldata = <MA>;
	close(MA);
	$sankasyasuu = @donuts_alldata;
	($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/,$saigonohito);
#do_yobi1 = 支払額
	if ($do_narandacard eq ""){$do_narandacard = 1;}
	$card_suu = length $do_narandacard;
#koko
	if ($card_suu * 20000 > $money){
		$motilimitdisp =($card_suu * 20000) / 10000;
		$hikeruka = "持ち金が$motilimitdisp万未満で引けません。\n";
	}else{
		$hikeruka = "<input type=submit value=\"カードを引く\">\n";
	}
#kokoend
	$my_card = "<img src=$img_dir/donuts/ura.gif width=64 heith=84>";
#引くコマンドだった場合
#koko2008/04/30
	if($renzokuhiki eq 'yes'){$hiku_kaisuu = 3;}else{$hiku_kaisuu = 1;}
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if($renzokuhiki eq 'yes'){
			(@tim_hiniti) = localtime($now_time);
			(@tim_hiniti_mae) = localtime($do_last);
			if ($name eq $do_name && $tim_hiniti[3] == $tim_hiniti_mae[3]){
				($do_name0,$do_hantei0,$do_hiitakard0,$do_narandacard0,$do_yobi10,$do_last0)= split(/<>/,$donuts_alldata[0]);
				(@tim_hiniti_mae) = localtime($do_last0);
				if ($name eq $do_name0 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
					($do_name1,$do_hantei1,$do_hiitakard1,$do_narandacard1,$do_yobi11,$do_last1)= split(/<>/,$donuts_alldata[1]);
					(@tim_hiniti_mae) = localtime($do_last1);
					if ($name eq $do_name1 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
						&error("同じ日に同じ方が続けてカードを引けるのは３回までです。");
					}
				}
			}
		}else{
			if ($name eq $do_name){&error("同じ方が続けてカードを引くことはできません");}
		}
#end2008/04/30
		foreach (@donuts_alldata){
			($do2_name,$do2_hantei,$do2_hiitakard,$do2_narandacard,$do2_yobi1,$do2_last)= split(/<>/);
			if ($name eq $do2_name){
				if ($now_time - $do2_last < 60*$crad_game_time){&error("最後にゲームしてからまだ$crad_game_time分すぎていません。");}
			}
		}
		$randed= int(rand(5))+1;
		$my_card_gazou = "$img_dir/donuts/"."$randed"."a.gif";
		$my_card = "<img src=$my_card_gazou width=64 heith=84>";
		$kingaku = $card_suu * 20000;
#アウトの場合
		if ($randed == $do_hiitakard){
			$money -= $kingaku;
			$do_hantei = "out";
			$do_narandacard = "$randed";
			$out_gaku = $card_suu*2;
			$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
			$siharai= $card_suu * 2;
			$card_suu = 1;
#セーフの場合
		}else{
			$money += $kingaku;
			$do_hantei = "safe";
			$siharai= $card_suu * 2;
			$do_narandacard = "$do_narandacard" . "$randed";
			$comment = "<div class=purasu>セーフ！！<br>$siharai万円をゲットしました！</div>";
		}
		$next_temp = "$name<>$do_hantei<>$randed<>$do_narandacard<>$siharai<>$now_time<>\n";
		unshift @donuts_alldata,$saigonohito;
		unshift @donuts_alldata,$next_temp;
		if ($sankasyasuu >= 19){pop @donuts_alldata;}
#データ更新
		&lock;
		open(KB,">$donuts2_logfile")|| &error("Open Error : $donuts2_logfile");
		eval{ flock (KB, 2); };
		print KB @donuts_alldata;
		close(KB);
		&unlock;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);		
	}		#引く場合の閉じ
	&header(gym_style);
			print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●ルール説明<br>
・参加者がすることはカードを１枚引くことだけです。<br>・引いたカードが前の人のカードと違っていれば、その時点でテーブルにたまっているカードの数×２万円のお金がもらえ、またそのカードがテーブルにたまっていきます。<br>・同じ数が出てしまった場合、逆にカードの数×２万円のお金を支払わなければいけません。またテーブルのカードは１枚からスタートとなります。<br>※同じ人が同じ日に続けてカードを$hiku_kaisuu回引くことが出来ます。※ゲーム間隔は$crad_game_time分です。</td>
<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>カードゲーム</b></font></td>
</tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
<div align=center>
$my_card
$comment
<form method="POST" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="donus2">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<!-- <input type=submit value="カードを引く"> -->
$hikeruka
</form></div>
EOM

	if ($do_hiitakard ne ""){
		$your_card = "$img_dir/donuts/$do_hiitakard" .".gif";
		print <<"EOM";
<div align=center><img src=$your_card width=60 heith=80></div>
<div align=center>前の人が引いたカード</div>
EOM
	}

	for ($i=0; $i < $card_suu; $i ++){
		$card_bangou = substr ($do_narandacard,$i,1);
		$table_card_image = "$img_dir/donuts/$card_bangou". ".gif";
		$line .= "<img src=$table_card_image width=30 height=40>\n";
	}

	print <<"EOM";
</td><td width=60% valign=top>
<div class=job_messe>＜現在までの引かれたカード＞</div>
<table  border="0" cellspacing="0" cellpadding="10" width=100% height=80% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
<tr><td>
$line
</td></tr></table>
</td></tr></table>
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>
<div class=honbun2>■最近のゲーム</div>
EOM
	if ($in{'command'} eq ""){
		unshift @donuts_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@donuts_alldata){
			($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/);
			$ikura = length $do_narandacard;
			if ($do_hantei eq "out"){
				print "<div class=mainasu>$do_nameさんが$do_yobi1万円を支払いました。</div>";
			}else{
				print "<div class=purasu>$do_nameさんが$do_yobi1万円をゲットしました。</div>";
			}
		}
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
}

####ドーナツゲーム３ koko 2005/03/10
sub donus3 {
	if ($tajuukinsi_flag==1){&tajuucheck;}
	open(MA,"< $donuts3_logfile") || &error("$donuts3_logfileが開けません");
	eval{ flock (MA, 1); };
	$saigonohito = <MA>;
	@donuts_alldata = <MA>;
	close(MA);
	$sankasyasuu = @donuts_alldata;
	($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/,$saigonohito);
#do_yobi1 = 支払額
	if ($do_narandacard eq ""){$do_narandacard = 1;}
	$card_suu = length $do_narandacard;
#koko
	if (100000 > $money){
		$motilimitdisp = 100000 / 10000;
		$hikeruka = "持ち金が$motilimitdisp万未満で引けません。\n";
	}else{
		$hikeruka = "<input type=submit value=\"カードを引く\">\n";
	}
#kokoend
	$my_card = "<img src=$img_dir/donuts/ura.gif width=64 heith=84>";
#引くコマンドだった場合
#koko2008/04/30
	if($renzokuhiki eq 'yes'){$hiku_kaisuu = 3;}else{$hiku_kaisuu = 1;}
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if($renzokuhiki eq 'yes'){
			(@tim_hiniti) = localtime($now_time);
			(@tim_hiniti_mae) = localtime($do_last);
			if ($name eq $do_name && $tim_hiniti[3] == $tim_hiniti_mae[3]){
				($do_name0,$do_hantei0,$do_hiitakard0,$do_narandacard0,$do_yobi10,$do_last0)= split(/<>/,$donuts_alldata[0]);
				(@tim_hiniti_mae) = localtime($do_last0);
				if ($name eq $do_name0 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
					($do_name1,$do_hantei1,$do_hiitakard1,$do_narandacard1,$do_yobi11,$do_last1)= split(/<>/,$donuts_alldata[1]);
					(@tim_hiniti_mae) = localtime($do_last1);
					if ($name eq $do_name1 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
						&error("同じ日に同じ方が続けてカードを引けるのは３回までです。");
					}
				}
			}
		}else{
			if ($name eq $do_name){&error("同じ方が続けてカードを引くことはできません");}
		}
#end2008/04/30
		foreach (@donuts_alldata){
			($do2_name,$do2_hantei,$do2_hiitakard,$do2_narandacard,$do2_yobi1,$do2_last)= split(/<>/);
			if ($name eq $do2_name){
				if ($now_time - $do2_last < 60*$crad_game_time){&error("最後にゲームしてからまだ$crad_game_time分すぎていません。");}
			}
		}
		$randed= int(rand(3))+1;
		$my_card_gazou = "$img_dir/donuts/"."$randed"."a.gif";
		$my_card = "<img src=$my_card_gazou width=64 heith=84>";
#セーフの場合
		if ($do_hiitakard eq ""){$do_hiitakard = 1;}#最初の一枚
		if ($randed == $do_hiitakard){
			$money += $card_suu * 100000;;
			$do_hantei = "safe";
			$siharai= $card_suu * 10;
			$do_narandacard = "$randed";
			$comment = "<div class=purasu>セーフ！！<br>$siharai万円をゲットしました！</div>";
			$card_suu = 1;
#アウトの場合
		}else{
			$money -= 100000;
			$do_hantei = "out";
			$do_narandacard = "$do_narandacard" . "$randed";
			$out_gaku = 1 * 10;
			$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
			$siharai= 1 * 10;
		}
		$next_temp = "$name<>$do_hantei<>$randed<>$do_narandacard<>$siharai<>$now_time<>\n";
		unshift @donuts_alldata,$saigonohito;
		unshift @donuts_alldata,$next_temp;
		if ($sankasyasuu >= 19){pop @donuts_alldata;}
#データ更新
		&lock;
		open(KB,">$donuts3_logfile")|| &error("Open Error : $donuts3_logfile");
		eval{ flock (KB, 2); };
		print KB @donuts_alldata;
		close(KB);
		&unlock;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
	}		#引く場合の閉じ
	&header(gym_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●ルール説明<br>
・参加者がすることはカードを１枚引くことだけです。<br>・引いたカードが前の人のカードと同じであれば、その時点でテーブルにたまっているカードの数×10万円のお金がもらえ、カードは１枚からスタートとなります。<br>・違う数が出てしまった場合、10万円のお金を支払わなければいけません。またテーブルにカードがたまっていきます。<br>※同じ人が同じ日に続けてカードを$hiku_kaisuu回引くことが出来ます。※ゲーム間隔は$crad_game_time分です。</td>
<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>カードゲーム</b></font></td>
</tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
<div align=center>
$my_card
$comment
<form method="POST" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="donus3">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<!-- <input type=submit value="カードを引く"> -->
$hikeruka
</form></div>
EOM

	if ($do_hiitakard ne ""){
		$your_card = "$img_dir/donuts/$do_hiitakard" .".gif";
		print <<"EOM";
<div align=center><img src=$your_card width=60 heith=80></div>
<div align=center>前の人が引いたカード</div>
EOM
	}

	for ($i=0; $i < $card_suu; $i ++){
		$card_bangou = substr ($do_narandacard,$i,1);
		$table_card_image = "$img_dir/donuts/$card_bangou". ".gif";
		$line .= "<img src=$table_card_image width=30 height=40>\n";
	}

	print <<"EOM";
</td><td width=60% valign=top>
<div class=job_messe>＜現在までの引かれたカード＞</div>
<table  border="0" cellspacing="0" cellpadding="10" width=100% height=80% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
<tr><td>
$line
</td></tr></table>
</td></tr></table>
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>
<div class=honbun2>■最近のゲーム</div>
EOM
	if ($in{'command'} eq ""){
		unshift @donuts_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@donuts_alldata){
			($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/);
			$ikura = length $do_narandacard;
			if ($do_hantei eq "out"){
				print "<div class=mainasu>$do_nameさんが$do_yobi1万円を支払いました。</div>";
			}else{
				print "<div class=purasu>$do_nameさんが$do_yobi1万円をゲットしました。</div>";
			}
		}
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
}

####ドーナツゲーム４,(Ｈ＆Ｌ)
sub donus4 {
	if ($tajuukinsi_flag==1){&tajuucheck;}
	
	open(MA,"< $donuts4_logfile") || &error("$donuts4_logfileが開けません");
	eval{ flock (MA, 1); };
	$saigonohito = <MA>;
	@donuts_alldata = <MA>;
	close(MA);
	
	$sankasyasuu = @donuts_alldata;
	($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/,$saigonohito);
	#do_yobi1 = 支払額
	if ($do_narandacard eq ""){$do_narandacard = 1;}
	$card_suu = length $do_narandacard;
    
	if ($card_suu * 10000 > $money){
		$motilimitdisp =($card_suu * 10000) / 10000;
		$hikeruka_hi = "持ち金が$motilimitdisp万未満で引けません。\n";
	}else{
		$hikeruka_hi = "<input type=submit value=\"大きい方に掛けてカードを引く\">\n";
		$hikeruka_low = "<input type=submit value=\"小さい方に掛けてカードを引く\">\n";
	}
    
	$my_card = "<img src=$img_dir/donuts/ura.gif width=64 heith=84>";
	
	#引くコマンドだった場合
	if($renzokuhiki eq 'yes'){$hiku_kaisuu = 3;}else{$hiku_kaisuu = 1;}
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if($renzokuhiki eq 'yes'){
			(@tim_hiniti) = localtime($now_time);
			(@tim_hiniti_mae) = localtime($do_last);
			if ($name eq $do_name && $tim_hiniti[3] == $tim_hiniti_mae[3]){
				($do_name0,$do_hantei0,$do_hiitakard0,$do_narandacard0,$do_yobi10,$do_last0)= split(/<>/,$donuts_alldata[0]);
				(@tim_hiniti_mae) = localtime($do_last0);
				if ($name eq $do_name0 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
					($do_name1,$do_hantei1,$do_hiitakard1,$do_narandacard1,$do_yobi11,$do_last1)= split(/<>/,$donuts_alldata[1]);
					(@tim_hiniti_mae) = localtime($do_last1);
					if ($name eq $do_name1 && $tim_hiniti[3] == $tim_hiniti_mae[3]){
						&error("同じ日に同じ方が続けてカードを引けるのは３回までです。");
					}
				}
			}
		}else{
			if ($name eq $do_name){&error("同じ方が続けてカードを引くことはできません");}
		}
        
		foreach (@donuts_alldata){
			($do2_name,$do2_hantei,$do2_hiitakard,$do2_narandacard,$do2_yobi1,$do2_last)= split(/<>/);
			if ($name eq $do2_name){
				if ($now_time - $do2_last < 60*$crad_game_time){&error("最後にゲームしてからまだ$crad_game_time分すぎていません。");}
			}
		}
		$randed= int(rand(5))+1;
		$my_card_gazou = "$img_dir/donuts/"."$randed"."a.gif";
		$my_card = "<img src=$my_card_gazou width=64 heith=84>";
		$kingaku = $card_suu * 10000;

		if ($randed == $do_hiitakard){
			$kingaku *= $doroubai;				
			#アウトの場合 倍率支払い
			if ($dorou eq 'アウト'){
				$money -= $kingaku;
				$do_hantei = "out";
				$do_narandacard = "$randed";
				$out_gaku = $card_suu * 1 * $doroubai;
				$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
				$siharai= $card_suu * 1 * $doroubai;
				$card_suu = 1;
			}else{
			#セーフの場合 倍率支払い
				$money += $kingaku;
				$do_hantei = "safe";
				$siharai= $card_suu * 1 * $doroubai;
				$do_narandacard = "$do_narandacard" . "$randed";
				$comment = "<div class=purasu>セーフ！！<br>$siharai万円をゲットしました！</div>";
			}
		}elsif ($randed < $do_hiitakard && $in{'kake'} eq 'hi' || $randed > $do_hiitakard && $in{'kake'} eq 'low'){
			#アウトの場合
			$money -= $kingaku;
			$do_hantei = "out";
			$do_narandacard = "$randed";
			$out_gaku = $card_suu * 1;
			$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
			$siharai= $card_suu * 1;
			$card_suu = 1;
		}else{
			#セーフの場合
			$money += $kingaku;
			$do_hantei = "safe";
			$siharai= $card_suu * 1;
			$do_narandacard = "$do_narandacard" . "$randed";
			$comment = "<div class=purasu>セーフ！！<br>$siharai万円をゲットしました！</div>";
		}
		$next_temp = "$name<>$do_hantei<>$randed<>$do_narandacard<>$siharai<>$now_time<>\n";
		unshift @donuts_alldata,$saigonohito;
		unshift @donuts_alldata,$next_temp;
		if ($sankasyasuu >= 19){pop @donuts_alldata;}
		
		#データ更新
		&lock;
		open(KB,">$donuts4_logfile")|| &error("Open Error : $donuts4_logfile");
		eval{ flock (KB, 2); };
		print KB @donuts_alldata;
		close(KB);
		&unlock;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
	}
	
	&header(gym_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●ルール説明<br>
・参加者がすることはカードを１枚引くことだけです。<br>・5枚のカードの引いたカードが前の人のカードより大きいか小さいか当てれば、その時点でテーブルにたまっているカードの数×１万円のお金がもらえ、またそのカードがテーブルにたまっていきます。<br>・違った場合、逆にカードの数×１万円のお金を支払わなければいけません。またテーブルのカードは１枚からスタートとなります。<br>・同じカードが出てしまった場合、$dorouとなり$doroubai倍となります。<br>※同じ人が同じ日に続けてカードを$hiku_kaisuu回引くことが出来ます。※ゲーム間隔は$crad_game_time分です。</td>
<td  bgcolor=#333333 align=center width=35%><img src="$img_dir/donuts_tytle.gif"></td>
</tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
<div align=center>
$my_card
$comment
<form method="POST" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="donus4">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=kake value="hi">
$hikeruka_hi
</form>
<form method="POST" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="donus4">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=kake value="low">
$hikeruka_low
</form>
</div>
EOM

	if ($do_hiitakard ne ""){
		$your_card = "$img_dir/donuts/$do_hiitakard" .".gif";
		print <<"EOM";
<div align=center><img src=$your_card width=60 heith=80></div>
<div align=center>前の人が引いたカード</div>
EOM
	}

	for ($i=0; $i < $card_suu; $i ++){
		$card_bangou = substr ($do_narandacard,$i,1);
		$table_card_image = "$img_dir/donuts/$card_bangou". ".gif";
		$line .= "<img src=$table_card_image width=30 height=40>\n";
	}

	print <<"EOM";
</td><td width=60% valign=top>
<div class=job_messe>＜現在までの引かれたカード＞</div>
<table  border="0" cellspacing="0" cellpadding="10" width=100% height=80% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
<tr><td>
$line
</td></tr></table>
</td></tr></table>
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>
<div class=honbun2>■最近のゲーム</div>
EOM

	if ($in{'command'} eq ""){
		unshift @donuts_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@donuts_alldata){
			($do_name,$do_hantei,$do_hiitakard,$do_narandacard,$do_yobi1,$do_last)= split(/<>/);
			$ikura = length $do_narandacard;
			if ($do_hantei eq "out"){
				print "<div class=mainasu>$do_nameさんが$do_yobi1万円を支払いました。</div>";
			}else{
				print "<div class=purasu>$do_nameさんが$do_yobi1万円をゲットしました。</div>";
			}
		}
	}
	
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
}
