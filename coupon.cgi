#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

###################リサイクル################################ 2006/12/22
# 商品保存ファイル名
$coupon_data_f = './dat_dir/coupon.cgi';
#################### unit.pl 追加 ##########
#"クーポン" => "<form method=POST action=\"coupon.cgi\"><td height=32 width=32><input type=hidden name=mode value=\"coupon\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=image src='$img_dir/reload.gif'  onMouseOver='onMes5(\"クーポン引換所です。\")' onMouseOut='onMes5(\"\")'></td></form>",

#############################################
$this_script = 'coupon.cgi';
#require './jcode.pl'; #2008/04/02 town_lib.pl sub decode { 変更のこと
#require './cgi-lib.pl'; #2008/04/02
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
	if($in{'mode'} eq "coupon"){&coupon;}
	if($in{'mode'} eq "coupon_do"){&coupon_do;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;


##### クーポン トップページ #########
sub coupon{
	#商品の表示
	open(IN,"< $coupon_data_f") || &error("Open Error : $coupon_data_f");
	eval{ flock (IN, 1); };
	@coupon_dat = <IN>;
	close(IN);
#koko2007/08/03
	if(!$k_id){&error("mono.cgi エラー coupon1")} #koko2007/11/18
	open(IN,"< ./member/$k_id/mono.cgi") || &error("Open Error : ./member/$k_id/mono.cgi");
	eval{ flock (IN, 1); };
	@mono_syohi = <IN>;
	close(IN);
	foreach (@mono_syohi){
		&syouhin_sprit($_);
		if ($syo_syubetu eq 'ギフト' && $syo_hinmoku eq 'クーポン'){
			$moterukazu = $syo_taikyuu;
			last;
		}
	}
	if (!$moterukazu){$moterukazu = '0';}

	&header_org;
#koko2005/03/17 表示位置替え1 03/18 <td colspan=26>→<td colspan=27>
	print <<"EOM";
<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>クーポン交換所です。<br>持っているクーポンは、$moterukazu 個です。<br></td>
<td  bgcolor=#ffcc00 align=center><br><h2>クーポン</h2></td>
</tr></table><br>
<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
※カロリーは摂取できる数値です。<br>
</font></td></tr>
<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>数</td><td>値段</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>売却<br>値段</td><!-- <td align=center nowrap>　備　考　</td> --><td align=center nowrap>購入日</td></tr>
EOM
	$i=0;
	foreach (@coupon_dat) {
		&syouhin_sprit($_);
		$now_time = time;
	#	$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
	#	$nokorinissuu = $kesunisuu - $keikanissuu;
	#	if ($nokorinissuu <= 0){next;}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
			print "<tr bgcolor=#ffff66><td colspan=26>▼$syo_syubetu</td></tr>";
		}
	#	if ($syo_taikyuu_tani eq "日"){
	#		$taikyuu_hyouzi_seikei = "$syo_taikyuu日";
	#	}else{
	#		$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
	#	}

	#	&byou_hiduke($syo_kounyuubi);

		if ($syo_comment){
			$disp_seru = "rowspan=\"2\"";
			$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=25>【 備考 】 $syo_comment</td></tr>";
		}else{
			$disp_seru = "";
			$disp_com = "";
		}
	#	$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
	#	if (!($syo_taikyuu <=0)){
			print <<"EOM";
<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="coupon_do">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=shiyori value="uru">
<input type=submit value="交換"><input type=hidden value="$i" name="koniyubangou"><input type=hidden name=syouhin value="$syo_hinmoku">$syo_hinmoku</form></td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$baikyaku_hyouzi</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$baikyaku_hyouzi円</td><!-- <td align=left>$syo_comment</td> --><td nowrap>$bh_tukihi</td></tr>$disp_com
EOM
		$i++;
	} #foreach閉じ

	print "</table>\n";

	&hooter("login_view","戻る");
	exit;
}

##### 買取処理 #################
sub coupon_do{
	open(IN,"< $coupon_data_f") || &error("Open Error : $coupon_data_f");
	eval{ flock (IN, 1); };	@koniyusiyouhin = <IN>;
	close(IN);

	if ($in{'koniyubangou'} eq ""){&error("購入番号がありません。");}
	$koniyusiyouhin = $koniyusiyouhin[$in{'koniyubangou'}];

	($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai)= split(/<>/,$koniyusiyouhin);
#koko2006/12/11
	$coupon_syubetu = $syo_syubetu;
	$coupon_taikyuu = $syo_taikyuu;
	if ($in{'syouhin'} ne $syo_hinmoku){&error("$in{'syouhin'} 購入番号と商品名が違ってます。もう一度確かめて。",'botan');} #errorを改造してあります。
##自分の持ち物を増やす
	if(!$k_id){&error("mono.cgi エラー coupon2")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
#koko2007/08/04
	$coupnf = 0;
	foreach (@myitem_hairetu) {
		&syouhin_sprit($_);
		if ($syo_syubetu eq 'ギフト' && $syo_hinmoku eq 'クーポン'){
			$coupnf = 1;
			($sybetu,$tensuu) = split(/:/,$coupon_syubetu);
			if ($syo_taikyuu - $tensuu < 0){
				&error("クーポンの点数が不足です。");
			}else{
				$syo_taikyuu -= $tensuu;
			}
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if (!$coupnf){&error("クーポンを持っていません。");}
#kokoend
	($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai)= split(/<>/,$koniyusiyouhin);

	$syo_kounyuubi = time;
	$baikyaku_hyouzi = ($tanka * $syo_taikyuu);

	&syouhin_temp;			#ver.1.3
	push (@new_myitem_hairetu,$syo_temp);			#ver.1.3

	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);
#ログ更新
#	&temp_routin;
#	&log_kousin($my_log_file,$k_temp);

	&header_org;
	print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$syo_hinmoku [$in{'koniyubangou'}]のクーポン交換をしました。
</span>
</td></tr></table>
<br>
<form method=POST action="$this_script">
<input type=hidden name=mode value="coupon">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="交換を続ける">
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
