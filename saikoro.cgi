#!/usr/bin/perl
# ↑お使いのサーバーのパスに合わせてください。

$this_script = 'saikoro.cgi';
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
	if($in{'mode'} eq "saikoro"){&saikoro;} #koko 2005/05/15

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

#sub unit_pl{
########################################################################
# unit.pl
#"サイコロ" => "<form method=POST action=\"saikoro.cgi\"><input type=hidden name=mode value=\"saikoro\"><input type=hidden name=mysec value=\"$in{'mysec'}\"><!-- koko2006/04/01 --><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/donuts_tate.gif'  onMouseOver='onMes5(\"サイコロで遊ぼう。\")' onMouseOut='onMes5(\"\")'></td></form>",
########################################################################
#}
############# サイコロゲーム #############
sub saikoro{

	# ログファイル名
	$saikoro_logfile = './log_dir/saikoro_log.cgi';
	# 持ち金制限 'yes'
	$motiganeseigen = 'no';
	# 連続可能か
	$sa_rentou = 'yes';
	# ゲーム間隔(分)
	$saikoro_game_time = 5;
	# 画像のフォルダー名
	$saikoro_img = "./img/daisu/";

	$rate = $in{'rate'};

	if ($tajuukinsi_flag==1){&tajuucheck;}
	open(MA,"$saikoro_logfile") || &error("$saikoro_logfileが開けません");
	@saicoro_dat = <MA>;
	close(MA);
	($sa_name,$sai_time,$sa_hantei,$saikoro_iti,$saikoro_ni,$kakekin,$saikoro_yobi)= split(/<>/,$saicoro_dat[0]);


	if ($rate > $money && $motiganeseigen eq 'yes'){
		$motilimitdisp = $rate / 10000;
		$hikeruka = "持ち金が$motilimitdisp万未満で引けません。\n";
	}else{
		$hikeruka = "<input type=submit value=\"偶数\" name=kake>\n";
		$hikeruka1 = "<input type=submit value=\"奇数\" name=kake>\n";
	}
#引くコマンドだった場合
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if ($name eq $sa_name && $sa_rentou ne 'yes'){&error("同じ方が続けてカードを引くことはできません");}
		foreach (@saicoro_dat){
			($sa_name,$sai_time,$sa_hantei,$saikoro_iti,$saikoro_ni,$kakekin,$saikoro_yobi)= split(/<>/);
				if ($name eq $sa_name){
					if ($now_time - $sai_time < 60*$saikoro_game_time){&error("最後にゲームしてからまだ$saikoro_game_time分すぎていません。");}
				}
		}

		$randed= int(rand(36));

		$saikoro_iti = int($randed / 6) + 1;
		$saikoro_ni = $randed % 6 +1;
		$goukei = $saikoro_iti + $saikoro_ni;
		if ($goukei % 2 == 0){$hntei = "偶数"}else{$hntei = "奇数"}
#アウトの場合
		if (($goukei % 2 == 0 && $in{'kake'} ne '偶数') || ($goukei % 2 == 1 && $in{'kake'} ne '奇数')){
			$money -= $rate;
			$sa_hantei = "out";
			$out_gaku = $rate /10000;
			$comment = "<div class=mainasu>アウトォーー！！<br>$out_gaku万円を支払いました！</div>";
#セーフの場合
		}else{
			$money += $rate;
			$sa_hantei = "safe";
			$siharai= $rate / 10000;
			$comment = "<div class=purasu>セーフ！！<br>$siharai万円をゲットしました！</div>";
		}
		$next_temp = "$name<>$now_time<>$sa_hantei<>$saikoro_iti<>$saikoro_ni<>$rate<>$saikoro_yobi<>\n";#ここは変える事
		unshift @saicoro_dat,$next_temp;
		if ($#saicoro_dat +1 >= 20){$#saicoro_dat =19;}
#データ更新
		&lock;
		open(KB,">$saikoro_logfile")|| &error("Open Error : $saikoro_logfile");
		print KB @saicoro_dat;
		close(KB);
		&unlock;
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);		
	}	#引く場合の閉じ
	&header(gym_style);
			print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●ルール説明<br>
	・参加者がすることはサイコロ２つの合計が偶数になるか奇数になるか当てます。<br>掛け金とどちらかを選びます。当たれば掛け金がもらえ、外れれば取られます。<br>※ゲーム間隔は$saikoro_game_time分です。</td>
	<td  bgcolor=#333333 align=center width=35%>
	<font color="#ffffff" size="5"><b>サイコロ</b></font>
	</td>
	</tr></table><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
	<div align=center>
	<!-- $saikoro_dis<br> -->
	$comment<br>$money円
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="saikoro">
	<input type=hidden name=command value="hiku">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<select name=rate>
<option value=10000>10000</option>
<option value=50000>50000</option>
<option value=100000>100000</option>
<option value=500000>500000</option>
<option value=1000000>1000000</option>
</select><br>
	$hikeruka $hikeruka1
	</form>
	</div>
EOM

	print <<"EOM";
	</td><td width=60% valign=top>
		<table  border="0" cellspacing="0" cellpadding="10" width=100% height=80% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
		<tr><td>
		<img src=$saikoro_img$saikoro_iti.gif><img src=$saikoro_img$saikoro_ni.gif>
		</td></tr></table>
	</td></tr></table>
	
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
	<div class=honbun2>■最近のゲーム</div>
EOM
	foreach (@saicoro_dat){
		($sa_name,$sai_time,$sa_hantei,$saikoro_iti,$saikoro_ni,$kakekin,$saikoro_yobi)= split(/<>/);
		$kakekin_dis = $kakekin / 10000;
		if ($sa_hantei eq 'out'){
			print "<div class=mainasu>$sa_nameさんが $saikoro_iti - $saikoro_ni で$kakekin_dis万円を支払いました。</div>";
		}else{
			print "<div class=purasu>$sa_nameさんが $saikoro_iti - $saikoro_ni で$kakekin_dis万円をゲットしました。</div>";
		}
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;

}
