#!/usr/bin/perl

#+++++++++++++++++++++++++++++++++++++
#  Copyright (c) チャゲ
#  web：http://tyage.a.orn.jp/
#パラメータ保管庫はチャゲが作りました
#+++++++++++++++++++++++++++++++++++++

$this_script = 'parabank.cgi';
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
	elsif($in{'mode'} eq "doukyo"){&doukyo;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
####同居人
sub doukyo {
		$chara_settei_file="./member/$k_id/parabank.cgi";
			if (! -e $chara_settei_file){
				open(CPB,">$chara_settei_file") || &error("Write Error : $chara_settei_file");
				eval{ flock (CPB, 2); };
				chmod 0666,"$chara_settei_file";
				close(CPB);
			}
		open(KSF,"< $chara_settei_file") || &error("Open Error : $chara_settei_file");
			$para = <KSF>;
		close(KSF);
		if ($in{'command'} eq "make_chara2"){
		
	@hankaku = ("$in{'ch2_kokugo'}","$in{'ch2_suugaku'}","$in{'ch2_rika'}","$in{'ch2_syakai'}","$in{'ch2_eigo'}","$in{'ch2_ongaku'}","$in{'ch2_bijutu'}","$in{'ch2_etti'}","$in{'ch2_looks'}","$in{'ch2_tairyoku'}","$in{'ch2_kenkou'}","$in{'ch2_speed'}","$in{'ch2_power'}","$in{'ch2_wanryoku'}","$in{'ch2_kyakuryoku'}","$in{'ch2_love'}","$in{'ch2_unique'}");
	foreach (@hankaku){
		if ($_ =~('[&!*()/ =,<>]')){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}elsif($_ =~/\\/){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}		
		if($_ =~ /[^0-9]/){&error("数値入力欄に数値以外が記入されてます");}
	}
			if($allpara>$para){$message_in .= "保管されているパラメータ以上は上げれません！<br>";}
			
			if ($in{'ch2_kokugo'}) { $para -= $in{'ch2_kokugo'}; $message_in .= "国語パラメータを$in{'ch2_kokugo'}あげました。<br>"; $kokugo +=$in{'ch2_kokugo'}; }
			if ($in{'ch2_suugaku'}) { $para -= $in{'ch2_suugaku'}; $message_in .= "数学パラメータを$in{'ch2_suugaku'}あげました。<br>"; $suugaku +=$in{'ch2_suugaku'};}
			if ($in{'ch2_rika'}) { $para -= $in{'ch2_rika'}; $message_in .= "理科パラメータを$in{'ch2_rika'}あげました。<br>"; $rika +=$in{'ch2_rika'};}
			if ($in{'ch2_syakai'}) { $para -= $in{'ch2_syakai'}; $message_in .= "社会パラメータを$in{'ch2_rika'}あげました。<br>"; $syakai +=$in{'ch2_syakai'};}
			if ($in{'ch2_eigo'}) { $para -= $in{'ch2_eigo'}; $message_in .= "英語パラメータを$in{'ch2_eigo'}あげました。<br>"; $eigo +=$in{'ch2_eigo'};}
			if ($in{'ch2_ongaku'}) { $para -= $in{'ch2_ongaku'}; $message_in .= "音楽パラメータを$in{'ch2_ongaku'}あげました。<br>"; $ongaku +=$in{'ch2_ongaku'};}
			if ($in{'ch2_bijutu'}) { $para -= $in{'ch2_bijutu'}; $message_in .= "美術パラメータを$in{'ch2_bijutu'}あげました。<br>"; $bijutu +=$in{'ch2_bijutu'};}
			if ($in{'ch2_looks'}) { $para -= $in{'ch2_looks'}; $message_in .= "ルックスパラメータを$in{'ch2_looks'}あげました。<br>"; $looks +=$in{'ch2_looks'};}
			if ($in{'ch2_tairyoku'}) { $para -= $in{'ch2_tairyoku'}; $message_in .= "体力パラメータを$in{'ch2_tairyoku'}あげました。<br>"; $tairyoku +=$in{'ch2_tairyoku'};}
			if ($in{'ch2_kenkou'}) { $para -= $in{'ch2_kenkou'}; $message_in .= "健康パラメータを$in{'ch2_kenkou'}あげました。<br>"; $kenkou +=$in{'ch2_kenkou'};}
			if ($in{'ch2_speed'}) { $para -= $in{'ch2_speed'}; $message_in .= "スピードパラメータを$in{'ch2_speed'}あげました。<br>"; $speed +=$in{'ch2_speed'};}
			if ($in{'ch2_power'}) { $para -= $in{'ch2_power'}; $message_in .= "パワーパラメータを$in{'ch2_power'}あげました。<br>"; $power +=$in{'ch2_power'};}
			if ($in{'ch2_wanryoku'}) { $para -= $in{'ch2_wanryoku'}; $message_in .= "腕力パラメータを$in{'ch2_wanryoku'}あげました。<br>"; $wanryoku +=$in{'ch2_wanryoku'};}
			if ($in{'ch2_kyakuryoku'}) { $para -= $in{'ch2_kyakuryoku'}; $message_in .= "脚力パラメータを$in{'ch2_kyakuryoku'}あげました。<br>"; $kyakuryoku +=$in{'ch2_kyakuryoku'};}
			if ($in{'ch2_love'}) { $para -= $in{'ch2_love'}; $message_in .= "LOVEパラメータを$in{'ch2_love'}あげました。<br>"; $love +=$in{'ch2_love'};}
			if ($in{'ch2_unique'}) { $para -= $in{'ch2_unique'}; $message_in .= "面白さパラメータを$in{'ch2_unique'}あげました。<br>"; $unique +=$in{'ch2_unique'};}
			if ($in{'ch2_etti'}) { $para -= $in{'ch2_etti'}; $message_in .= "エッチパラメータを$in{'ch2_etti'}あげました。<br>";  $etti +=$in{'ch2_etti'};}
			&make;
		}elsif ($in{'command'} eq "make_chara"){
		
	@hankaku = ("$in{'ch_kokugo'}","$in{'ch_suugaku'}","$in{'ch_rika'}","$in{'ch_syakai'}","$in{'ch_eigo'}","$in{'ch_ongaku'}","$in{'ch_bijutu'}","$in{'ch_etti'}","$in{'ch_looks'}","$in{'ch_tairyoku'}","$in{'ch_kenkou'}","$in{'ch_speed'}","$in{'ch_power'}","$in{'ch_wanryoku'}","$in{'ch_kyakuryoku'}","$in{'ch_love'}","$in{'ch_unique'}");
	foreach (@hankaku){
		if ($_ =~('[&!*()/ =,<>]')){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}elsif($_ =~/\\/){
			&error("使用禁止文字が含まれています<BR>[&!*()/=.,<>]半角スペース\\");
		}		
		if($_ =~ /[^0-9]/){&error("数値入力欄に数値以外が記入されてます");}
	}
			if ($in{'ch_kokugo'} && $kokugo > $in{'ch_kokugo'}) {$para += $in{'ch_kokugo'};$message_in .= "パラメータを$in{'ch_kokugo'}保管しました。<br>";$kokugo -=$in{'ch_kokugo'}; }
			if ($in{'ch_suugaku'} && $suugaku > $in{'ch_suugaku'}) { $para += $in{'ch_suugaku'};$message_in .= "パラメータを$in{'ch_suugaku'}保管しました。<br>";$suugaku -=$in{'ch_suugaku'};}
			if ($in{'ch_rika'} && $rika > $in{'ch_rika'}) { $para += $in{'ch_rika'};$message_in .= "パラメータを$in{'ch_rika'}保管しました。<br>";$rika -=$in{'ch_rika'};}
			if ($in{'ch_syakai'} && $syakai > $in{'ch_syakai'}) { $para += $in{'ch_syakai'}; $message_in .= "パラメータを$in{'ch_rika'}保管しました。<br>"; $syakai -=$in{'ch_syakai'};}
			if ($in{'ch_eigo'} && $eigo > $in{'ch_eigo'}) { $para += $in{'ch_eigo'}; $message_in .= "パラメータを$in{'ch_eigo'}保管しました。<br>"; $eigo -=$in{'ch_eigo'};}
			if ($in{'ch_ongaku'} && $ongaku > $in{'ch_ongaku'}) { $para += $in{'ch_ongaku'}; $message_in .= "パラメータを$in{'ch_ongaku'}保管しました。<br>"; $ongaku -=$in{'ch_ongaku'};}
			if ($in{'ch_bijutu'} && $bijutu > $in{'ch_bijutu'}) { $para += $in{'ch_bijutu'}; $message_in .= "パラメータを$in{'ch_bijutu'}保管しました。<br>"; $bijutu -=$in{'ch_bijutu'};}
			if ($in{'ch_looks'} && $looks > $in{'ch_looks'}) { $para += $in{'ch_looks'}; $message_in .= "パラメータを$in{'ch_looks'}保管しました。<br>"; $looks -=$in{'ch_looks'};}
			if ($in{'ch_tairyoku'} && $tairyoku > $in{'ch_tairyoku'}) { $para += $in{'ch_tairyoku'}; $message_in .= "パラメータを$in{'ch_tairyoku'}保管しました。<br>"; $tairyoku -=$in{'ch_tairyoku'};}
			if ($in{'ch_kenkou'} && $kenkou > $in{'ch_kenkou'}) { $para += $in{'ch_kenkou'}; $message_in .= "パラメータを$in{'ch_kenkou'}保管しました。<br>"; $kenkou -=$in{'ch_kenkou'};}
			if ($in{'ch_speed'} && $speed > $in{'ch_speed'}) { $para += $in{'ch_speed'}; $message_in .= "パラメータを$in{'ch_speed'}保管しました。<br>"; $speed -=$in{'ch_speed'};}
			if ($in{'ch_power'} && $power > $in{'ch_power'}) { $para += $in{'ch_power'}; $message_in .= "パラメータを$in{'ch_power'}保管しました。<br>";  $power -=$in{'ch_power'};}
			if ($in{'ch_wanryoku'} && $wanryoku > $in{'ch_wanryoku'}) { $para += $in{'ch_wanryoku'}; $message_in .= "パラメータを$in{'ch_wanryoku'}保管しました。<br>"; $wanryoku -=$in{'ch_wanryoku'};}
			if ($in{'ch_kyakuryoku'} && $kyakuryoku > $in{'ch_kyakuryoku'}) { $para += $in{'ch_kyakuryoku'}; $message_in .= "パラメータを$in{'ch_kyakuryoku'}保管しました。<br>"; $kyakuryoku -=$in{'ch_kyakuryoku'};}
			if ($in{'ch_love'} && $love > $in{'ch_love'}) { $para += $in{'ch_love'}; $message_in .= "パラメータを$in{'ch_love'}保管しました。<br>"; $love -=$in{'ch_love'};}
			if ($in{'ch_unique'} && $unique > $in{'ch_unique'}) { $para += $in{'ch_unique'}; $message_in .= "パラメータを$in{'ch_unique'}保管しました。<br>"; $unique -=$in{'ch_unique'};}
			if ($in{'ch_etti'} && $etti > $in{'ch_etti'}) { $para += $in{'ch_etti'}; $message_in .= "パラメータを$in{'ch_etti'}保管しました。<br>"; $etti -=$in{'ch_etti'};}
			&make;
			
			}else{
	
#画面表示
		&header(item_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td bgcolor=#ffffff>ここでは自分のパラメータをやり取りできます。<br>
	上のところで自分のパラメータを保管庫に移すことで、保管庫のパラメータが増え、自分のパラメータが減ります。<br>
	その後、下のところで保管庫のパラメータを自分に移すことで、自分のパラメータが増え、保管庫のパラメータが減ります。<br>
	（※保管してあるパラメータ以上は増やせません！）<br>
	何に使うかはあなた次第ですが、仕事などに使うといいでしょう。<br></td>
	</tr></table><br>
EOM

#所有物チェック koko 2005/04/16
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(MK,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (MK, 2); };
	@my_kounyuu_list =<MK>;
	close(MK);
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}
	#kokoend

	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="doukyo">
	<input type=hidden name=command value="make_chara">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
		<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
		<tr><td align="center">
	<div class=honbun2>●パラメーター保管</div>
	入力した数値分のパラメーターが自分から引かれ、手数料１万円がかかります。<br>
	保管庫に、与えられた数値分のパラメーターが保管されます。<br>
	<table border="0"><tr>
	<td>国語</td><td><input type=text name="ch_kokugo" size=10></td></td>
	<td>数学</td><td><input type=text name="ch_suugaku" size=10></td>
	<td>理科</td><td><input type=text name="ch_rika" size=10></td>
	<td>社会</td><td><input type=text name="ch_syakai" size=10></td>
	<td>英語</td><td><input type=text name="ch_eigo" size=10></td></tr><tr>
	<td>音楽</td><td><input type=text name="ch_ongaku" size=10></td>
	<td>美術</td><td><input type=text name="ch_bijutu" size=10></td>
	<td>ルックス</td><td><input type=text name="ch_looks" size=10></td>
	<td>体力</td><td><input type=text name="ch_tairyoku" size=10></td>
	<td>健康</td><td><input type=text name="ch_kenkou" size=10></td></tr><tr>
	<td>スピード</td><td><input type=text name="ch_speed" size=10></td>
	<td>パワー</td><td><input type=text name="ch_power" size=10></td>
	<td>腕力</td><td><input type=text name="ch_wanryoku" size=10></td>
	<td>脚力</td><td><input type=text name="ch_kyakuryoku" size=10></td>
	<td>LOVE</td><td><input type=text name="ch_love" size=10></td></tr><tr>
	<td>面白さ</td><td><input type=text name="ch_unique" size=10></td>
	<td>エッチ</td><td><input type=text name="ch_etti" size=10>
	</tr></table>

	</td></tr>
	<tr><td colspan=3>
	<div align=center>
支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select><!-- koko -->

	<input type=submit value="記入分を自分から減らし、保管する"></div>
	</td></tr></table>
	<br>
	<center>保管されているパラメータの合計:$para</center><br>
	
	</form>
	
	
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="doukyo">
	<input type=hidden name=command value="make_chara2">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
		<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
		<tr><td align="center">
	<div class=honbun2>●パラメーターアップ</div>
	入力した数値分のパラメーターが保管庫から引かれ、手数料１万円がかかります。<br>
	自分のパラメータが入力した分だけ増えます。（※保管してあるパラメータ以上は増やせません！）<br>
	<table border="0"><tr>
	<td>国語</td><td><input type=text name="ch2_kokugo" size=10></td></td>
	<td>数学</td><td><input type=text name="ch2_suugaku" size=10></td>
	<td>理科</td><td><input type=text name="ch2_rika" size=10></td>
	<td>社会</td><td><input type=text name="ch2_syakai" size=10></td>
	<td>英語</td><td><input type=text name="ch2_eigo" size=10></td></tr><tr>
	<td>音楽</td><td><input type=text name="ch2_ongaku" size=10></td>
	<td>美術</td><td><input type=text name="ch2_bijutu" size=10></td>
	<td>ルックス</td><td><input type=text name="ch2_looks" size=10></td>
	<td>体力</td><td><input type=text name="ch2_tairyoku" size=10></td>
	<td>健康</td><td><input type=text name="ch2_kenkou" size=10></td></tr><tr>
	<td>スピード</td><td><input type=text name="ch2_speed" size=10></td>
	<td>パワー</td><td><input type=text name="ch2_power" size=10></td>
	<td>腕力</td><td><input type=text name="ch2_wanryoku" size=10></td>
	<td>脚力</td><td><input type=text name="ch2_kyakuryoku" size=10></td>
	<td>LOVE</td><td><input type=text name="ch2_love" size=10></td></tr><tr>
	<td>面白さ</td><td><input type=text name="ch2_unique" size=10></td>
	<td>エッチ</td><td><input type=text name="ch2_etti" size=10>
	</tr></table>

	</td></tr>
	<tr><td colspan=3>
	<div align=center>
支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select><!-- koko -->

	<input type=submit value="記入分を保管庫から減らし、自分に移す"></div>
	</td></tr></table>
	</form>
	
EOM
	}
	

		&hooter("login_view","戻る");
		exit;
}

sub make{
			if($para =~ /[^0-9]/){&error("数値が不適切です");}
			if ($para < 0){&error("数値が不適切です");}
			if ($para != 0){
				$message_in .= "手数料１万円を支払いました。。<br>";
			}
#koko 2005/04/16
			if ($in{'siharaihouhou'} ne "現金"){
				$bank -= 10000;
				if ($c_kane_bank){ #koko 2005/05/05
					&kityou_syori("クレジット支払い（Ｃリーグ支払い）","$c_kane_bank","",$bank,"普");
				}
			}else{
				if ($money < 10000){&error("お金が足りません");}
				$money -= 10000;
			}
#パワーのMAX値計算
			$make_ch_temp ="$para";
	&lock;
	open(MTLO,">$chara_settei_file") || &error("Write Error : $chara_settei_file");
	eval{ flock (MTLO, 2); };
	print MTLO $make_ch_temp;
	close(MTLO);
	&unlock;
					&temp_routin;
					&log_kousin($my_log_file,$k_temp);
	&message("$message_in","doukyo","parabank.cgi");
}