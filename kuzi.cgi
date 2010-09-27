#!/usr/bin/perl

############################
#同じ人が続けてできるかどうか（１．できる　０.できない）
$kuzi_set1 = 1;
#↑で１を選んだときの時間間隔（分）０だとすきなだけまわせます＠＠
$kuzi_set2 = 3;
#１ゲームあたりの料金（ここを増やしたり変えればいろんな料金になります）
@kuzi_set3 = ('500','1000','5000','10000','50000','100000','500000','1000000');
#くじの代金を所持して無くてもできるか（０．できない　１.できる）
$kuzi_set4 = 0;
# 当たった時元金を引く　('yes','no')
$atri_moto_hiku = 'yes';
#くじのログファイル
$kuzi_log = "./log_dir/kuzi_log.cgi";
# 管理
$kuzikanre = "./log_dir/kuzi_kanre.cgi";
# 記憶時間（分）
$kioku_time = 10;
#画像ファイルのディレクトリ
$img_dir2 = "./sugoroku/img/";
#履歴数max
$kirokusu = 20;
############################

$this_script = 'kuzi.cgi';
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
	if($in{'mode'} eq "kuzi_game"){&kuzi_game;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub kuzi_game {

	&header(ginkou_style);

	#データ読み込み
	open(MA,"$kuzi_log") || &error("$kuzi_logが開けません");
	$kuzi_data = <MA>;
	@kuzi_kiroku = <MA>;
	close(MA);
	($kuzi_name,$kuzi_time,$kuzi_count,$koshin)= split(/<>/,$kuzi_data);
	if ($kuzi_name eq $in{'name'} && $in{'command2'} eq $koshin && $in{'command2'} eq "seisan"){
		&error("二重記帳エラー","teturn");
	}
	if($in{'command'} eq "hiku"){
		open(MA,"$kuzikanre") || &error("$kuzikanreが開けません");
		@kuzi_kanri = <MA>;
		close(MA);
		$ima_time = time;
		foreach (@kuzi_kanri){
			($ku_name,$dabulu,$ku_time) = split(/<>/);
			if($ku_time && $ku_time + $kioku_time * 60 < $ima_time){
				next;
			}
			if ($in{'name'} eq $ku_name){
				$kaisu = $dabulu;
				$ku_time = $ima_time;
			}
			$shin_dat = "$ku_name<>$dabulu<>$ku_time<>\n";
			push @new_kuzi_kanri,$shin_dat;
		}
		if (!$kaisu){
			$kaisu = 1;
			$shin_dat = "$in{'name'}<>1<>$ima_time<>\n";
			unshift @new_kuzi_kanri,$shin_dat;
		}
	#	open(MA,"> $kuzikanre") || &error("$kuzikanreが開けません");
	#	eval{ flock (MA, 2); };
	#	print MA @new_kuzi_kanri;
	#	close(MA);

		$kakekin = "$in{'rate'} * (2 ** $kaisu)";
		if($in{'command2'} ne "seisan"){
			if($in{'sentaku_card'} == ""){
				&error("カードを選んでください。");
			}
			$now_time = time ;
			if ($kaisu < 2){
				#前回のゲームをした人と自分が一緒かを調べる
				if($kuzi_name eq "$name"){
				#同じ人だった場合が出来るか
					if($kuzi_set1 == 1){
						#出来る場合の時間間隔処理
						if($kuzi_time + $kuzi_set2*60 > $now_time){
							&error("同じ人がプレーにするは$kuzi_set2分まってください。");
						}
					}else{	#同じ人はできない）
						&error("同じ人は続けてプレーすることが出来ません。");
					}
				}
			}
			#所持金ちぇっく
			if($in{'rate'} > $money && $kuzi_set4==0){
				&error("所持金が足りません。");
			}
			print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<div class=purasu align=center>＋＋＋結果発表\＋＋＋</div>
<table border="0" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="200"><tr>
EOM
			$randed=int(rand(2))+1;
#test $randed =1; #test
			for($i=1;$i < 3 ;$i ++){
				if($in{'sentaku_card'} == $i){
					$koredaro="<div align=center>↑<br>選んだカード</div>";}else{$koredaro="";
				}
				if($i == $randed){
					print "<td><img src=$img_dir2/atari.gif width=90 height=110>$koredaro</td>\n";
				}else{
					print "<td><img src=$img_dir2/hazure.gif width=90 height=110>$koredaro</td>\n";
				}
			}
			print "</tr><tr><td colspan=4>";
#当たった場合
			if($in{'sentaku_card'} == $randed){
				$bairitu = 2 ** $kaisu;
				$syoukin=$in{'rate'} * (2 ** $kaisu);
				print "<div class=purasu align=center>見事当たりました！掛け金の$bairitu倍になります！$syoukin円！</div>\n";
				$coment = "<font color=\"#008000\">見事当たりました！掛け金の$bairitu倍になります！$syoukin円！</font>";
				foreach (@new_kuzi_kanri){
					($ku_name,$dabulu,$ku_time) = split(/<>/);
					if ($in{'name'} eq $ku_name){
						$dabulu++;
						$ku_time = $ima_time;
					}
					$shin_dat = "$ku_name<>$dabulu<>$ku_time<>\n";
					push @newkuzikanri,$shin_dat;
				}
				open(MA,"> $kuzikanre") || &error("$kuzikanreが開けません");
				eval{ flock (MA, 2); };
				print MA @newkuzikanri;
				close(MA);

#はずれた場合
			}else{
				foreach (@new_kuzi_kanri){
					($ku_name,$dabulu,$ku_time) = split(/<>/);
					if ($in{'name'} eq $ku_name){
						next;
					}
					$shin_dat = "$ku_name<>$dabulu<>$ku_time<>\n";
					push @newkuzikanri,$shin_dat;
				}
				open(MA,"> $kuzikanre") || &error("$kuzikanreが開けません");
				eval{ flock (MA, 2); };
				print MA @newkuzikanri;
				close(MA);

				$syoukin = $in{'rate'} * (2 ** $kaisu);
				if ($in{'rate'} == $syoukin){

					print "<div class=mainasu align=center>はずれてしまいました。残念ながら$in{'rate'}円は没収です。</div>\n";
					&hooter("login_view","戻る");
					$coment = "<font color=\"#ff0000\">はずれてしまいました。残念ながら$in{'rate'}円は没収です。</font>";
				}else{

					print "<div class=mainasu align=center>はずれてしまいました。残念ながら$in{'rate'}円は没収で$syoukinはなしです。</div>\n";
					&hooter("login_view","戻る");
					$coment = "<font color=\"#ff0000\">はずれてしまいました。残念ながら$in{'rate'}円は没収で$syoukinはなしです。</font>";
				}
			
				$money -= $in{'rate'};


			}

			if ($in{'sentaku_card'} == $randed){

				print <<"EOM";
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="kuzi_game">
<input type=hidden name=command value="">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=rate value="$in{'rate'}">
<input type="submit" value="ダブルアップに挑戦">
</form>
<form method=\"POST\" action="$this_script">
<input type=hidden name=mode value="kuzi_game">
<input type=hidden name=command value="hiku">
<input type=hidden name=command2 value="seisan">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=rate value="$in{'rate'}">
<input type="submit" value="精算する">
</form>
EOM
			}
			print "</td></tr></table>";

		}else{
			print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<div class=purasu align=center>＋＋＋結果発表\＋＋＋</div>
<table border="0" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="200"><tr>
EOM
			$bairitu = 2 ** ($kaisu - 1);
			$syoukin = $in{'rate'} * (2 ** ($kaisu - 1));
		
			#所持金変更処理
			#所持金-かけた金額+かけた金額*倍率
			if ($atri_moto_hiku eq 'yes'){
				$money = $money - $in{'rate'} + $syoukin;
				$moraeru_kane = $syoukin - $in{'rate'};
				$disp_kane = " = $moraeru_kane";
				print "<div class=purasu align=center>精算して、掛け金の$bairitu倍の！$syoukin - $in{'rate'}$disp_kane円ゲット！</div>\n";
				&hooter("login_view","戻る");
				$coment = "<font color=\"#008000\">精算して、掛け金の$bairitu倍の！$syoukin - $in{'rate'}$disp_kane円ゲット！</font>";
				print "</td></tr></table>";
			}else{
				if ($syoukin != 0){
					$money += $syoukin;
					print "<div class=purasu align=center>精算して、掛け金の$bairitu倍の！$syoukin円ゲット！</div>\n";
					&hooter("login_view","戻る");
					$coment = "<font color=\"#008000\">精算して、掛け金の$bairitu倍の！$syoukin円ゲット！</font>";
					print "</td></tr></table>";
				}
			}
			foreach (@new_kuzi_kanri){
				($ku_name,$dabulu,$ku_time) = split(/<>/);
				if ($in{'name'} eq $ku_name){
					next;
				}
				$shin_dat = "$ku_name<>$dabulu<>$ku_time<>\n";
				push @newkuzikanri,$shin_dat;
			}
			open(MA,"> $kuzikanre") || &error("$kuzikanreが開けません");
			eval{ flock (MA, 2); };
			print MA @newkuzikanri;
			close(MA);

		}
		#個人データ更新
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
		#くじのデータ更新
		$kuzi_count++;
		$kuzi_new_data = "$name<>$now_time<>$kuzi_count<>$in{'command2'}<>\n";
		$kuzi_new_data2 = "$name<>$now_time<>$kuzi_count<>$coment<>$in{'command2'}<>\n";
		unshift(@kuzi_kiroku,$kuzi_new_data2);
		if($kirokusu -1 < $#kuzi_kiroku){$#kuzi_kiroku = $kirokusu-1;}

		&lock;
		open(KB,">$kuzi_log")|| &error("Open Error : $kuzi_log");
		print KB $kuzi_new_data;
		print KB @kuzi_kiroku;
		close(KB);
		
		&unlock;
		print <<"EOM";
<table border="1"  align=center class=yosumi>
<TR><TD align=center>
<center>
現在の所持金：$money円<BR>
<TD><TR>
</table></table>
EOM

	}else{		#if（引くコマンドだったら）の閉じ

	if (!$in{'rate'}){
	#掛け金表示処理
		$rate="<select name=rate>";
		foreach (@kuzi_set3){
			$rat=$_;
			if($kuzi_set4==1 ||($kuzi_set4==0 && $rat <= $money)){
			#掛け金の表示部分でのカンマ表示処理
				if ($rat =~ /^[-+]?\d\d\d\d+/g) {for ($i = pos($rat) - 3, $j = $rat =~ /^[-+]/; $i > $j; $i -= 3) {substr($rat, $i, 0) = ',';}}
				$rate.="<option value=$_>$rat</option>\n";
			}else{
				last;
			}
		}
		$rate.="</select>";
	}else{
		$rate = $in{'rate'} * (2 ** $kaisu);
	}

		print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<TR><TD align=center>
<center><div class=purasu align=center>＋＋＋カードゲーム＋＋＋</div><br>
現在の所持金：$money円<BR>
</TD><TR>
</table>
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="3" align="center" width="80%">
<tr><td>

<form method="POST" action="$this_script">
<input type=hidden name=mode value="kuzi_game">
<input type=hidden name=command value="hiku">
<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=id value="$in{'id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=gamerand value="$in{'gamerand'}">
EOM
	if ($in{'rate'}){
		print "<input type=hidden name=rate value=\"$in{'rate'}\">\n";
	#	print "<input type=hidden name=dabulu value=\"$kaisu\">\n";
	}

		print <<"EOM";
<table border="0" cellspacing="0" cellpadding="3" align="center" width="200">
<tr>
<td align="center">
<img src="$img_dir2/card_sentaku.gif" width="90" height="110"><br>
<input type="radio" name="sentaku_card" value="1">
</td>
<td align="center">
<img src="$img_dir2/card_sentaku.gif" width="90" height="110">
<input type="radio" name="sentaku_card" value="2">
</td>
</tr></table>
<div align="center">掛け金$rate円<br>
<input type="submit" value="これでいい"></div>
</form>
<div class="honbun">※２枚のカードのうち１枚が当たりです。当たりを引けば掛け金の２倍かのお金がもらえる権利が出来ます。そして、倍額にチャレンジする資格を得ます。精算をするかチャレンジするかはあなた次第。精算までにはずれてしまうと掛け金は没収となります。参加費は引かれて精算されます。精算をしないとお金はもらえません。</div>
</td>
</tr>
</table>
EOM
	}		#else（引くコマンドで無い場合）の閉じ
	print "<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\" align=\"center\" width=\"80%\" bgcolor=\"#ffffff\">\n";
	print "<tr><td>\n";
	print "<b>今までの記録</b><br>\n";
	foreach (@kuzi_kiroku){
		($kuzi_name,$kuzi_time,$kuzi_count,$coment)= split(/<>/);
		print "$kuzi_nameさんがチャレンジ！$coment<br>\n";
	}
	print "</td></tr></table>\n";
	print "<div align=\"right\">オリジナル:ゆかにゃん<br>Edit:たっちゃん<div>\n";

	&hooter("login_view","戻る");
	exit;
}		#sub閉じ

