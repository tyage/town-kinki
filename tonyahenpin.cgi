#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

########################################################################

# 交換の手数料
$tesuuryou = 0.75;

$this_script = 'tonyahenpin.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
$seigenyou_now_time = time;
#制限時間チェック
#		$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
#		if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
	if($in{'mode'} eq "henpin"){&henpin;}
	elsif($in{'mode'} eq "henpin_do"){&henpin_do;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
#############################
sub henpin {
	$syouhi_file="./member/$in{'k_id'}/omise_log.cgi";
	open(OUT,"< $syouhi_file") || &error("Open Error : $syouhi_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);

	@alldata = (@myitem_hairetu);

	&header(item_style);
	print <<"EOM";
<form method="POST" action="$this_script">
<input type=hidden name=mode value="henpin_do">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>
※自分で作成した「ギフト」はメール送信画面のセレクトメニューに現れます。<br>
<td  bgcolor=#00ff00 align=center width="200"><h1>問屋返品</h1></td>
</tr></table><br>
<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
<tr><td colspan=27><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
※カロリーは摂取できる数値です。<br>
</font></td></tr>
<tr bgcolor=#00ff><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>単価</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>耐久</td><td align=center nowrap>　備　考　</td><td align=center nowrap></td></tr>
EOM
	$now_time = time;			#ver.1.3
	@new_myitem_hairetu = ();
	$basyo = 1; #
	foreach (@alldata) {
		&syouhin_sprit($_);

		$no_dis = "";
		if ($maeno_syo_syubetu ne "$syo_syubetu"){
			print "<tr bgcolor=#87cefa><td colspan=27>▼$syo_syubetu</td></tr>";
		}
		$no_dis = "<input type=radio name=\"basyo\" value=\"$basyo\t$syo_nedan\t$syo_hinmoku\">";
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}

			print <<"EOM";
<tr bgcolor=#b0e0e6 align=center><td nowrap align=left>$no_dis $syo_hinmoku</td><td nowrap>$syo_zaiko</td><td>$syo_nedan</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$syo_taikyuu$syo_taikyuu_tani</td><td align=left>$syo_comment</td><td nowrap>$bh_tukihi</td></tr>
EOM
		$maeno_syo_syubetu = "$syo_syubetu";
		$basyo++; #
	}		#foreach閉じ
	if (! @alldata){print "<tr><td colspan=27>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
<tr><td colspan=27>
<div align=center>
<input type=\"text\" name=\"henkansu\" size=\"3\" value=\"\" maxlength=\"3\"><!--koko-->
<input type=submit value=" O K "></div></td></tr>
</table></form>
EOM
	&hooter("login_view","戻る");
	exit;
}
#######アイテム売却
sub henpin_do {
	($basyo,$syo_nedan,$syo_hinmoku) = split(/\t/,$in{'basyo'});
	if ($basyo eq ""){&error("アイテムが選ばれていません$basyo,$syo_nedan。");}
	$syouhi_file="./member/$in{'k_id'}/omise_log.cgi";
	open(OUT,"< $syouhi_file") || &error("Open Error : $syouhi_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;#koko2006/10/20
	close(OUT);

	$omise_settei_file="./member/$in{'k_id'}/omise_ini.cgi";
	open(OIB,"< $omise_settei_file") || &error("お店設定ファイルが開けません。家でお店を開いているか確認してください");
	eval{ flock (OIB, 1); };
	$omise_settei_data = <OIB>;
	($omise_title,$omise_come,$omise_body_style,$omise_syubetu)= split(/<>/,$omise_settei_data);
	close(OIB);
	if ($omise_syubetu eq "スーパー"){
		$suupaa = 1.5;
	}else{$suupaa = 1;}

	$kosu = $in{'henkansu'};

	if ($kosu){                                                                                                             
		if ($kosu =~ m/\D/){
			&error("数字のみを受け付けます。");
		}
	}

	syouhin_sprit($myitem_hairetu[$in{'basyo'} - 1]);
	if ($kosu <= 0 || $kosu >= $syo_zaiko){
		$haraimodoshi = int($syo_zaiko * $syo_nedan * $suupaa * $tesuuryou);
		$bank += $haraimodoshi;
		&kityou_syori("返品（$syo_hinmoku $syo_nedan円 $syo_zaiko個）","","$haraimodoshi",$bank,"普");
		$basyodasi = $in{'basyo'} - 1;
		splice (@myitem_hairetu,$basyodasi,1);
	}else{
		$syo_zaiko -= $kosu;
		$haraimodoshi = int($kosu * $syo_nedan * $suupaa * $tesuuryou);
		$bank += $haraimodoshi;
		&kityou_syori("返品（$syo_hinmoku $syo_nedan円 $kosu個）","","$haraimodoshi",$bank,"普");
		&syouhin_temp;
		$myitem_hairetu[$in{'basyo'} - 1] = $syo_temp;
	}

	open(OUT,">$syouhi_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @myitem_hairetu;
	close(OUT);

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&henpin;
}
