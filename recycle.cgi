#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

###################リサイクル################################ 2006/12/22
# 商品保存ファイル名
$recycle_log_f = './log_dir/recycle_log.cgi';
# 売却上限
$uritobasi_jyougen = 200000;
# 在庫数
$re_zaiko = 50;
# 保存日数
$kesunisuu = 7;
# 持っているギフトを売れるか　'yes' 売れる 'no' 売られない
$gyfturi = "yes";
# 売り飛ばし規制 2007/10/16 1*24*60*60
$uritobasi_kisei = 30*60;


#################### unit.pl 追加 ##########
#"リサイ" => "<form method=POST action=\"recycle.cgi\"><td height=32 width=32><input type=hidden name=mode value=\"resycle\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=image src='$img_dir/reload.gif'  onMouseOver='onMes5(\"リサイクルショップです。\")' onMouseOut='onMes5(\"\")'></td></form>",

#############################################
$this_script = 'recycle.cgi';
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
	if($in{'mode'} eq "resycle"){&resycle;}
	if($in{'mode'} eq "resycle_do"){&resycle_do;}
	if($in{'mode'} eq "baikyaku"){&baikyaku;}
	if($in{'mode'} eq "baikyaku_do"){&baikyaku_do;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;


##### リサイクル トップページ #########
sub resycle{
	#商品の表示
	open(IN,"< $recycle_log_f") || &error("Open Error : $recycle_log_f");
	@recycle_dat = <IN>;
	close(IN);

	&header_org;
#koko2005/03/17 表示位置替え1 03/18 <td colspan=26>→<td colspan=27>
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>リサイクルショップです。<br>要らない持ち物を売ったり買うことが出来ます。<br>$re_zaiko個または$kesunisuu日販売いたします。それ以上は自動的に消えていきます。<br>買取上限は$uritobasi_jyougen円です。買った場合、種別はリサイクルとなります。食料品とファーストフードはそのままです。。<br>
	現在の$nameさんの身体エネルギー：$energy　頭脳エネルギー：$nou_energy</td>
	<td  bgcolor=#ffcc00 align=center><br><h2>リサイクル</h2></td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。<br>
	</font></td></tr>
		<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>数</td><td>値段</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>売却<br>値段</td><!-- <td align=center nowrap>　備　考　</td> --><td align=center nowrap>購入日</td></tr>
EOM
	$i=0;
	foreach (@recycle_dat) {
		&syouhin_sprit($_);
		$now_time = time;
		$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
		$nokorinissuu = $kesunisuu - $keikanissuu;
		if ($nokorinissuu <= 0){next;}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
			print "<tr bgcolor=#ffff66><td colspan=26>▼$syo_syubetu</td></tr>";
		}
		if ($syo_taikyuu_tani eq "日"){
			$taikyuu_hyouzi_seikei = "$syo_taikyuu日";
		}else{
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
		}

		&byou_hiduke($syo_kounyuubi);

		if ($syo_comment){
			$disp_seru = "rowspan=\"2\"";
			$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=25>【 備考 】 $syo_comment</td></tr>";
		}else{
			$disp_seru = "";
			$disp_com = "";
		}
		$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
		if (!($syo_taikyuu <=0)){
			print <<"EOM";
<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="resycle_do">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=shiyori value="uru">
<input type=submit value="買う"><input type=hidden value="$i" name="koniyubangou"><input type=hidden name=syouhin value="$syo_hinmoku">$syo_hinmoku</form></td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$baikyaku_hyouzi</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$baikyaku_hyouzi円</td><!-- <td align=left>$syo_comment</td> --><td nowrap>$bh_tukihi</td></tr>$disp_com

EOM
		}
		&syouhin_temp;
		push (@my_hairetu,$syo_temp);
		if($#my_hairetu >= $re_zaiko -1){$#my_hairetu = $re_zaiko-1;}
		$syo_hinmoku = "";
		$i++;
	} #foreach閉じ
	open(OUT,">$recycle_log_f") || &error("Write Error : $recycle_log_f");
	eval{ flock (OUT, 2); };
	print OUT @my_hairetu;
	close(OUT);

	print <<"EOM";

	<tr><td colspan=26>
	<div align=center>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="baikyaku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
 <input type=hidden name=shiyori value="kau"><input type=submit value="売る"></form></table>
EOM

	&hooter("login_view","戻る");
	exit;
}

##### 買取処理 #################
sub resycle_do{
	open(IN,"< $recycle_log_f") || &error("Open Error : $recycle_log_f");
	@koniyusiyouhin = <IN>;
	close(IN);

	if ($in{'koniyubangou'} eq ""){&error("購入番号がありません。");}
	$koniyusiyouhin = $koniyusiyouhin[$in{'koniyubangou'}];

	($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai)= split(/<>/,$koniyusiyouhin);
#koko2006/12/11
	if ($in{'syouhin'} ne $syo_hinmoku){&error("$in{'syouhin'} 購入番号と商品名が違ってます。もう一度確かめて。",'botan');} #errorを改造してあります。
#kokoend
	if (!($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード")){
		$syo_syubetu = "リサイクル";
	}
	$syo_kounyuubi = time;
	$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
	$money -= $baikyaku_hyouzi;
#koko2007/10/16
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	@myitem_hairetu = <OUT>;
	close(OUT);
	&syouhin_temp;
	push (@myitem_hairetu,$syo_temp);

	$itemsu = 0;
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		unless($syo_syubetu eq 'ギフト' || $syo_syubetu eq 'ギフト商品'){$itemsu++;}
	}
	$itemsu--;
	if($itemsu >= $syoyuu_gendosuu){&error("持ち物がいっぱいです。$itemsu");}
#kokoend
###売り場の商品を減らす
	splice @koniyusiyouhin,$in{'koniyubangou'},1;

	open(OUT,">$recycle_log_f") || &error("Write Error : $recycle_log_f");
	eval{ flock (OUT, 2); };
	print OUT @koniyusiyouhin;
	close(OUT);	

##自分の持ち物を増やす 2007/10/16 場所移動
#	$monokiroku_file="./member/$k_id/mono.cgi";
#	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
#	@myitem_hairetu = <OUT>;
#	close(OUT);

#	&syouhin_temp;			#ver.1.3
#	push (@myitem_hairetu,$syo_temp);			#ver.1.3

	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @myitem_hairetu;
	close(OUT);
	$loop_count = 0;
	while ($loop_count <= 10){
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @myitem_hairetu ne ""){
		#	sleep(1);
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&header_org;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$syo_hinmoku [$in{'koniyubangou'}]($baikyaku_hyouzi円)を仕入れました。
</span>
</td></tr></table>
<br>
	<form method=POST action="$this_script">
	<input type=hidden name=mode value="resycle">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="購入を続ける">
	</form>
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form>
	</div>
	</body></html>
EOM
	exit;
}

##### 持ち物売却 ############
sub baikyaku{
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	@myitem_hairetu = <OUT>;
	close(OUT);

	$i = 0;
	foreach $data (@myitem_hairetu){
		$aitm_hiretu = (split(/<>/,$data))[0];

		$kuka_basyo = (split(/<>/,$data))[9];
		if ($kuka_basyo =~ /食料品/ and $aitm_hiretu eq "ギフト商品"){
			$aitm_hiretu = "食料品";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "食料品";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		if ($kuka_basyo =~ /ファ/ and $aitm_hiretu  eq "ギフト商品"){
			$aitm_hiretu = "ファーストフード";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "ファーストフード";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		$i++;

		if ($aitm_hiretu eq "ギフト商品"){
			push @aitem_giftsyo,$data;
		}elsif ($aitm_hiretu eq "ギフト"){ #koko2006/12/31
			push @aitem_gift,$data; #koko2006/12/31
		}else{
			push @aitem_sonota,$data;
		}
	}
	@keys0 = map {(split /<>/)[21]} @aitem_giftsyo;
	@itemgift = @aitem_giftsyo[sort {$keys0[$a] <=> $keys0[$b]} 0 .. $#keys0];
#koko2006/12/31
	@keys0 = map {(split /<>/)[21]} @aitem_gift;
	@gift = @aitem_gift[sort {$keys0[$a] <=> $keys0[$b]} 0 .. $#keys0];
#kokoend2006/12/31
	@keys0 = map {(split /<>/)[0]} @aitem_sonota;
	@itemsonota = @aitem_sonota[sort {$keys0[$a] cmp $keys0[$b]} 0 .. $#keys0];
#koko2006/12/31
	if ($gyfturi eq "yes"){
		@alldata = (@itemgift,@itemsonota,@gift);
	}else{
		@alldata = (@itemgift,@itemsonota);
	}
#kokoend2006/12/31
	&header_org;
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="baikyaku_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>売却したいアイテムにチェックをいれ、「使用する」か「売却する」を選んでOKボタンを押してください。<br>
	※備考に（※アイコン）とある商品は、持っていることで新しいアイコンが現れます。「使用」してしまうと無くなってしまい効果も消えますのでご注意ください。<br>
	※自分で購入した「ギフト」はメール送信画面のセレクトメニューに現れます。このリストには表\示されません。<br>
	現在の$nameさんの身体エネルギー：$energy　頭脳エネルギー：$nou_energy</td>
	<td bgcolor="#ffcc00" align=center width=300><font color="#ffffff" size="5"><b>アイテム</b></font></td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。<br>
	</font></td></tr>
		<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>使用</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>売却<br>値段</td><!-- <td align=center nowrap>　備　考　</td> --><td align=center nowrap>購入日</td></tr>
EOM
	$now_time = time;
	@new_myitem_hairetu = ();
	foreach (@alldata) {
		&syouhin_sprit($_);
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
		}
		if ($syo_taikyuu <=0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
			print "<tr bgcolor=#ffff66><td colspan=26>▼$syo_syubetu</td></tr>";
		}

		if ($syo_taikyuu_tani eq "日"){
			$taikyuu_hyouzi_seikei = "$nokorinissuu日";
			$baikyaku_hyouzi = ($tanka * $nokorinissuu);
		}else{
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
		}

		&byou_hiduke($syo_kounyuubi);

		if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
			$disp_siyukanou = "－";
		}else{$disp_siyukanou = "OK";}

		if(($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && $now_time < $last_syokuzi + ($syokuzi_kankaku*60)){ 
			$disp_siyukanou = "－";
		}
		if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール' && $syo_sake > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート' && $syo_dezato > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク' && $syo_dorinku > time){
			$disp_siyukanou = "－";
		}
		if ($syo_comment){
			$disp_seru = "rowspan=\"2\"";
			$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=25>【 備考 】 $syo_comment</td></tr>";
		}else{
			$disp_seru = "";
			$disp_com = "";
		}
		if (!($syo_taikyuu <=0)){
			if($disp_siyukanou eq "OK"){ #koko2007/10/16
				$disp_radio = "<input type=radio value=\"$syo_hinmoku\t$syo_syubetu\" name=\"syo_hinmoku\">";
			}else{$disp_radio = "";} #end2007/10/16

			print <<"EOM";
		<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>$disp_radio$syo_hinmoku</td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$disp_siyukanou</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$baikyaku_hyouzi円</td><!-- <td align=left>$syo_comment</td> --><td nowrap>$bh_tukihi</td></tr>$disp_com
EOM
		}
		if ($syo_taikyuu > 0){
			$maeno_syo_syubetu = "$syo_syubetu";
		}
	}	#foreach閉じ
	if (! @alldata){print "<tr><td colspan=26>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
	<tr><td colspan=26>
	<div align=center>
	<input type=hidden name=command value="baikyaku">
	<input type=submit value="売却する"></div></td></tr>
	</table></form>
EOM
	&hooter("login_view","戻る");
	exit;
}

##### 売却処理 ###########
sub baikyaku_do{
	if ($in{'syo_hinmoku'} eq ""){&error("アイテムが選ばれていません。");}
	($in_syo_hinmoku,$in_syo_syubetu) = split(/\t/,$in{'syo_hinmoku'});#2006/11/29
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	@myitem_hairetu = <OUT>;
	close(OUT);
	$siyouzumi_flag = 0;
	foreach  (@myitem_hairetu) {
		&syouhin_sprit($_);
		if($in{'command'} eq "baikyaku" && $syo_hinmoku eq $in_syo_hinmoku && $syo_syubetu eq $in_syo_syubetu && !$furagu){
			$now_time = time;
			if ($now_time < $syo_kounyuubi + $uritobasi_kisei){ #koko2007/10/16
				$print_messe .= "●$in_syo_hinmokuの売却は未だ出来ません。";
			}else{
				if ($syo_taikyuu_tani eq "日"){
					$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
					$nokorinissuu = $syo_taikyuu - $keikanissuu;
					$baikyaku_hyouzi = ($tanka * $nokorinissuu);
					if ($baikyaku_hyouzi > $uritobasi_jyougen){
						$baikyaku_hyouzi = $uritobasi_jyougen;
					$tanka = int(($baikyaku_hyouzi / $nokorinissuu) * 0.8);
					}
#koko2007/01/01
					if ($keikanissuu == 0){&error('日数が1日経過していませんのでこの商品はお取り扱い出来ません。');}
					$syo_kounyuubi = $now_time;
					$syo_taikyuu = $nokorinissuu;
#kokoend
				}else{
					$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
					if ($baikyaku_hyouzi > $uritobasi_jyougen){
						$baikyaku_hyouzi = $uritobasi_jyougen;
					}

					$tanka = int(($baikyaku_hyouzi / $syo_taikyuu) * 0.8);
				}
				if ($baikyaku_hyouzi > $uritobasi_jyougen){
					$baikyaku_hyouzi = $uritobasi_jyougen;
				}

				if($syo_syubetu eq 'ギフト商品'){
					$syo_comment_t = $syo_comment;
					($syo_comment)= split(/。/,$syo_comment_t);
					$syo_comment .="。";
				}
				$syo_kounyuubi = time;
				$furagu = 1;
				#商品リサイクルに入れる
				open(IN,"< $recycle_log_f") || &error("Open Error : $recycle_log_f");
				@recycle_dat = <IN>;
				close(IN);

				&syouhin_temp;
				unshift (@recycle_dat,$syo_temp);

				open(OUT,">$recycle_log_f") || &error("Write Error : $recycle_log_f");
				eval{ flock (OUT, 2); };
				print OUT @recycle_dat;
				close(OUT);	

				$money += $baikyaku_hyouzi;
				$print_messe .= "●$in_syo_hinmokuを売却し、$baikyaku_hyouzi円を得ました。";#koko2006/11/29
				next;
			}		
		}#if（「売却」コマンドだった場合）の閉じ
		
		if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}	#foreachの閉じ

#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
#自分の所有物ファイルを更新
#	&lock;
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
#koko2006/11/02
	$loop_count = 0;
	while ($loop_count <= 10){
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @new_myitem_hairetu ne ""){
		#	sleep(1);
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#	&unlock;
			
	&header_org;
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
	<span class="job_messe">
	$print_messe
	</span>
	</td></tr></table>
	<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="baikyaku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=shiyori value="kau">
	<input type=submit value="続けて売る"></form>

<!-- <div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div> -->
	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
	exit;
}
################# ヘッダー 
sub header_org{
#	print "Content-type:text/html; charset=Shift_JIS\n\n";
	print "Content-type:text/html;\n\n"; #2006/12/22
print <<"EOF";
<html>
<head>
<META http-equiv="content-type" content="text/html; charset=Shift_JIS">
<title>$title</title>
<style type="text/css">
<!--
.item_style { background-color:#ffcc66; background-image:url(./img/command_bak.gif)}	/*アイテム使用画面の背景*/
.yosumi {  border: #666666; border-style: solid; border-top-width: 1px; border-right-width: 1px; border-bottom-width: 1px; border-left-width: 1px; background-color:#ffffff}	/*街ステータス窓*/
a {color:#333333;text-decoration: none}
body {font-size:13px;color:#000000 }
table {font-size:13px;color:#000000;}
-->
</style>
</head><body style="" class=item_style leftmargin=5 topmargin=5 marginwidth=5 marginheight=5>
EOF
}

__END__
