
sub motimono_hanbai{
#	呼び出し前に  # ($in{'ori_ie_id'},$bangou)が行われている。
	($in{'ori_ie_id'},$bangou2) = split(/_/, $in{'ori_ie_id'});
	$kaisya_id = $in{'ori_ie_id'};
#	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."$bangou";

	$motimono_file = "./member/$kaisya_id/3_log.cgi"; #koko2007/04/21
	open(IN,"$motimono_file") || &error("Open Error : $motimono_file");
	eval{ flock (IN, 2); };
	$my_para = <IN>;
	@mono_list = <IN>;
	close(IN);

	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}

	&header(syokudou_style);
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>闇市です。品揃えは家の持ち主が変えます。単品処理のため同じ物を買うと、使う時に一緒になくなります。また一度に持てる所有物の限度は$syoyuu_gendosuu品目です。<div class="honbun2">●$nameさんの所持金：$money円</div></td>
	<td  bgcolor=#555555 align=center>闇市</td>
	</tr></table><br>
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br></font>
	<font color=#ff6600>※ギフトは贈り物専用の商品です。自分で使用することはできません。</font></td></tr>
<tr><td colspan=26><div align=center>
<!--	支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select></div> --> </td></tr>
		<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>値段</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td></tr>
EOM
	$i=0;
	foreach (@mono_list) {
		&syouhin_sprit2($_);

		if ($zokusei && $k_id ne $kaisya_id){
			$disp_seru = "rowspan=\"2\"";
			$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=23>【 倉庫品 】【 備考 】 $syo_comment</td></tr>";
			$i++;
			next;
		}else{
			$disp_seru = "rowspan=\"2\"";
			$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=23>【 備考 】 $syo_comment</td></tr>";
		}

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

	#	&byou_hiduke($syo_kounyuubi);
			print <<"EOM";
<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>
<form method="POST" action="mothimonohanbai.cgi">
<input type=hidden name=mode value="mothi_do">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=submit value="買う"><input type=hidden value="$i" name="koniyubangou"><input type=hidden name=syouhin value="$syo_hinmoku">$syo_hinmoku<br>支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select></form></td><td nowrap>$taikyuu_hyouzi_seikei</td><td align=right nowrap>$syo_nedan円</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
		$i++;
	} #foreach閉じ

	if ($k_id eq $kaisya_id){
		print <<"EOM";
	<tr><td colspan=26>
	<div align=center>
	<form method="POST" action="mothimonohanbai.cgi">
	<input type=hidden name=mode value="mothi_baikyaku">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=k_id value="$k_id">
	<input type=hidden name=town_no value="$town_no">
	<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
	<input type=submit value="売る/預ける"></form></table>
EOM
	}else{
		print "</table>\n";
	}

	&hooter("login_view","戻る");
	exit;
}



sub syouhin_sprit2{
	($syo_syubetu,$syo_hinmoku,$syo_kokugo,$syo_suugaku,$syo_rika,$syo_syakai,$syo_eigo,$syo_ongaku,$syo_bijutu,$syo_kouka,$syo_looks,$syo_tairyoku,$syo_kenkou,$syo_speed,$syo_power,$syo_wanryoku,$syo_kyakuryoku,$syo_nedan,$syo_love,$syo_unique,$syo_etti,$syo_taikyuu,$syo_taikyuu_tani,$syo_kankaku,$syo_zaiko,$syo_cal,$syo_siyou_date,$syo_sintai_syouhi,$syo_zunou_syouhi,$syo_comment,$syo_kounyuubi,$tanka,$tokubai,$zokusei)= split(/<>/,@_[0]);
chomp $zokusei;
}

sub syouhin_temp2{
	$syo_temp2="$syo_syubetu<>$syo_hinmoku<>$syo_kokugo<>$syo_suugaku<>$syo_rika<>$syo_syakai<>$syo_eigo<>$syo_ongaku<>$syo_bijutu<>$syo_kouka<>$syo_looks<>$syo_tairyoku<>$syo_kenkou<>$syo_speed<>$syo_power<>$syo_wanryoku<>$syo_kyakuryoku<>$syo_nedan<>$syo_love<>$syo_unique<>$syo_etti<>$syo_taikyuu<>$syo_taikyuu_tani<>$syo_kankaku<>$syo_zaiko<>$syo_cal<>$syo_siyou_date<>$syo_sintai_syouhi<>$syo_zunou_syouhi<>$syo_comment<>$syo_kounyuubi<>$tanka<>$tokubai<>$zokusei<>\n";
}












1;
