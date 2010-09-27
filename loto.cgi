#!/usr/bin/perl

#######################
#ロトの成績を記録する最低桁数（0ならボッシュートを含めて全部表す）
$kirokuketa=0;
#ロトの成績ログファイル
$loto_logfile="./log_dir/loto_kiroku.cgi";
#同じ人が続けてできるかどうか（１．できる　０.できない）
$loto_set1=1;
#↑で１を選んだときの時間間隔（分）
$loto_set2=3;
#１ゲームあたりの料金（ここを増やしたり変えればいろんな料金になります）
@loto_set3=('500','1000','5000','10000','50000','100000');
#ロトの代金を所持して無くてもできるか（０．できない　１.できる）
$loto_set4=0;
#ロトのログファイル
$loto_log="./log_dir/loto_log.cgi";
#######################

$this_script = 'loto.cgi';
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
	if($in{'mode'} eq "loto_game"){&loto_game;}
	else{&error("「戻る」ボタンで街に戻ってください");}
	
exit;

sub loto_game {

	&header(ginkou_style);

	#成績ファイルを開く
	open(MA,"$loto_logfile") || &error("$loto_logfileが開けません");
	$saigonohito = <MA>;
	@loto_alldata = <MA>;
	close(MA);
	$sankasyasuu = @loto_alldata;
	($do_name,$do_kakekin,$do_ketasuu,$do_kakutoku,$do_time)= split(/<>/,$saigonohito);

		#データ読み込み
		open(MA,"$loto_log") || &error("$loto_logが開けません");
		$loto_data = <MA>;
		close(MA);
		($loto_name,$loto_time,$loto_count)= split(/<>/,$loto_data);
		$now_time = time ;
		#前回のゲームをした人と自分が一緒かを調べる
		if($loto_name eq "$name"){
			#同じ人だった場合が出来るか
			if($loto_set1 == 1){
				#出来る場合の時間間隔処理
				if($loto_time + $loto_set2*60 > $now_time){
					&error("同じ人がプレーにするは$loto_set2分まってください。");
				}
			}else{
				#同じ人はできない）
				&error("同じ人は続けてプレーすることが出来ません。");
			}
		}
		#所持金ちぇっく
		if($in{'rate'} > $money && $loto_set4==0){
			&error("所持金が足りません。");
		}

	if($in{'command'} eq "hiku"){


				print <<"EOM";
				<div class=midasi align=center>＋＋＋結果発表\＋＋＋</div><br>
				<table border=0 bgcolor=#ffffff cellspacing=0 cellpadding=0 align=center width=400>
EOM
				$loto1=int(rand(10));
				$loto2=int(rand(10));
				$loto3=int(rand(10));
				$loto4=int(rand(10));
				$loto5=int(rand(10));
				$loto6=int(rand(10));
		print <<"EOM";
<tr><td colspan=6><div class=mainasu align=center>◆◆◆当選数字◆◆◆</div></td></tr>
<tr class=sumi><td class=loto align=center>$loto1</td>
<td class=loto align=center>$loto2</td><td class=loto align=center>$loto3</td>
<td class=loto align=center>$loto4</td><td class=loto align=center>$loto5</td>
<td class=loto align=center>$loto6</td></tr>
<tr><td align=center class=purasu>↓</td>
<td align=center class=purasu>↓</td>
<td align=center class=purasu>↓</td>
<td align=center class=purasu>↓</td>
<td align=center class=purasu>↓</td>
<td align=center class=purasu>↓</td></tr>
<tr class=sumi><td class=loto align=center>$in{'loto1'}</td>
<td class=loto align=center>$in{'loto2'}</td>
<td class=loto align=center>$in{'loto3'}</td>
<td class=loto align=center>$in{'loto4'}</td>
<td class=loto align=center>$in{'loto5'}</td>
<td class=loto align=center>$in{'loto6'}</td></tr>
<tr><td colspan=6><div class=purasu align=center>$nameさんの選んだ数字</div>
EOM
#当たった場合
					$atari = 0;
					if($loto1 == $in{'loto1'}){$atari ++;}
					if($loto2 == $in{'loto2'}){$atari ++;}
					if($loto3 == $in{'loto3'}){$atari ++;}
					if($loto4 == $in{'loto4'}){$atari ++;}
					if($loto5 == $in{'loto5'}){$atari ++;}
					if($loto6 == $in{'loto6'}){$atari ++;}
					if($atari == 0){
							print "<div align=center class=mainasu>残念ながら一つも当たらなかったので$in{'rate'}円は没収です！</div>\n";
								$bai=0;
								$do_ketasuu=0;
					}elsif($atari == 1){
							$syoukin=$in{'rate'}*2;
							print "<div align=center  class=purasu>１桁当たりました！$syoukin 円獲得！</div align=center >\n";
								$bai=2;
								$do_ketasuu=1;
					}elsif($atari == 2){
							$syoukin=$in{'rate'}*5;
							print "<div align=center  class=purasu>２桁当たりました！$syoukin 円獲得！</div align=center >\n";
								$bai=5;
								$do_ketasuu=2;
					}elsif($atari == 3){
							$syoukin=$in{'rate'}*20;
							print "<div align=center  class=purasu>おめでとうございます。３桁当たりました！$syoukin 円獲得！</div align=center >\n";
								$bai=20;
								$do_ketasuu=3;
					}elsif($atari == 4){
							$syoukin=$in{'rate'}*100;
							print "<div align=center  class=purasu>やりました！４桁当たりました！$syoukin 円獲得！</div align=center >\n";
								$bai=100;
								$do_ketasuu=4;
					}elsif($atari == 5){
							$syoukin=$in{'rate'}*500;
							print "<div align=center  class=purasu>すごいです！５桁当たりました！$syoukin 円獲得！</div align=center >\n";
								$bai=500;
								$do_ketasuu=5;
					}elsif($atari == 6){
							$syoukin=$in{'rate'}*1000;
							print "<div align=center  class=purasu>す、す、すごいです！！６桁当たりました！！$syoukin 円獲得です！！！！</div align=center >\n";
								$bai=1000;
								$do_ketasuu=6;
					}
				print "</td></tr></table>";

		#所持金変更処理
		#所持金-かけた金額+かけた金額*倍率
		$money = $money - $in{'rate'} + $in{'rate'} * $bai;
		print "<input type=hidden name=pass value=\"$in{'rate'}\">\n";
		$do_kakekin=$in{'rate'};
		$do_kakutoku=$do_kakekin*$bai;
		unshift @loto_alldata,$saigonohito;
		if ($do_ketasuu>=$kirokuketa){
		$next_temp = "$name<>$do_kakekin<>$do_ketasuu<>$do_kakutoku<>$now_time<>\n";
		unshift @loto_alldata,$next_temp;
		if ($sankasyasuu >= 49){pop @loto_alldata;}
		#データ更新
		&lock;
		open(KB,">$loto_logfile")|| &error("Open Error : $loto_logfile");
		print KB @loto_alldata;
		close(KB);
		&unlock;
		}


		#個人データ更新
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);

		#ロトのデータ更新
		$loto_count++;
		$loto_new_data="$name<>$now_time<>$loto_count<>\n";
		
		&lock;
		open(KB,">$loto_log")|| &error("Open Error : $loto_log");
		print KB $loto_new_data;
		close(KB);
		
		&unlock;
		print <<"EOM";
		<table border="1"  align=center class=yosumi>
		<TD align=center>
		<BR><BR>
		<center>
		現在の所持金：$money円<BR>
		<BR><BR>
</table>
EOM
	
	}else{		#if（引くコマンドだったら）の閉じ



	#掛け金表示処理
	$rate="<select name=rate>";
	foreach (@loto_set3)
		{
		$rat=$_;
		if($loto_set4==1 ||($loto_set4==0 && $rat <= $money))
			{
			#掛け金の表示部分でのカンマ表示処理
			if ($rat =~ /^[-+]?\d\d\d\d+/g) {for ($i = pos($rat) - 3, $j = $rat =~ /^[-+]/; $i > $j; $i -= 3) {substr($rat, $i, 0) = ',';}}
			$rate.="<option value=$_>$rat</option>\n";
			}
		else
			{
			last;
			}
		}
	$rate.="</select>";
		print <<"EOM";
		<table border="1"  align=center class=yosumi>
		<TD align=center>
		<BR><BR>
		<center>
		現在の所持金：$money円<BR>
		<BR><BR>
</table>
<table border=0  bgcolor=#ffffff cellspacing=0 cellpadding=3 align=center width=600>
<tr><td>
EOM
	print <<"EOM";
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="loto_game">
<input type=hidden name=command value="hiku">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<div class=midasi align=center>LOTO6ゲーム</div><div align=center>現在までの総プレイヤー数：$loto_count</div>
<table border=\"0\" cellspacing=\"0\" cellpadding=\"3\" align=\"center\" width=\"400\"><tr><td colspan=6>
<div class=honbun>６桁の数字を予\想\して一攫千金を目指しましょう！　各桁の数字が１桁当たると掛け金の2倍、２桁当たると5倍、３桁当たると20倍、４桁当たると100倍、５桁当たると500倍、そして６桁すべて当たると何と1000倍もらえます！！最高1億円が当たる！<br>
ただし全部はずした場合、掛け金はボッシュートです</div>
<br></td></tr><tr>
EOM

for ($a=1;$a < 7; $a ++){
		print "<td><select name=loto$a>";
		$c=int(rand(10));
		for ($b=0; $b < 10; $b ++){
				if($b == $c){print "<option value=$b selected>$b</option>";}else{
				  print "<option value=$b>$b</option>";}
		}
		print "</select></td>";
}
	print "</tr></table><br><div align=center>掛け金$rate円<br><input type=submit value=\"これでいい\"></div></form></td></tr></table>";
	}		#else（引くコマンドで無い場合）の閉じ

	if($kirokuketa==0){
		$gamecom="";}
	else{
		$gamecom="（$kirokuketa桁以上当てた人のみ）";
	}

	print <<"EOM";
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
	<div class=honbun2>■最近のゲーム$gamecom</div>
EOM


	if ($in{'command'} eq ""){
		unshift @loto_alldata,$saigonohito;
	}
	if (length $saigonohito != 0){
		foreach (@loto_alldata){
			($do_name,$do_kakekin,$do_ketasuu,$do_kakutoku,$do_time)= split(/<>/);

			# 時刻を得る
			($sec,$min,$hour,$day,$mon,$year) = localtime($do_time);
			$mon++;
			# yy/mm/dd の日付形式に書式を整える
			$date = sprintf("%02d/%02d %02d:%02d",$mon,$day,$hour,$min);

				if ($do_ketasuu==0){
					print "<div class=mainasu>$do_nameさんは$do_kakekin円をかけましたがボッシュート！　　[$date]</div>";
				}else{
					print "<div class=purasu>$do_nameさんが$do_kakekin円をかけ、$do_ketasuu桁当てました！$do_kakutoku円ゲット！　[$date]</div>";
				}
		}
	}
	print <<"EOM";
	</td></tr></table>
EOM

	&hooter("login_view","戻る");
	exit;
}		#sub閉じ

