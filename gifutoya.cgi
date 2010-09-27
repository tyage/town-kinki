#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
			#2006/10/20 OUT
########################################################################
# unit.pl
#sub unit_pl{
#"ギフト屋" => "<form method=POST action=\"gifutoya.cgi\"><input type=hidden name=mode value=gifutoya><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/item.gif'  onMouseOver='onMes5(\"ギフト変換所\")' onMouseOut='onMes5(\"\")'></td></form>",
#}
########################################################################

# 交換の手数料
$koukan_money = 50000;

$this_script = 'gifutoya.cgi';
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
	if($in{'mode'} eq "gifutoya"){&gifutoya;}
	elsif($in{'mode'} eq "gifutoya_do"){&gifutoya_do;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
#############################
sub gifutoya {
	if(!$k_id){&error("mono.cgi エラー gifutoya1")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;#koko2006/10/20
	close(OUT);
	foreach $data (@myitem_hairetu){
		$aitm_hiretu = (split(/<>/,$data))[0];
		if ($aitm_hiretu eq "ギフト商品"){
			push @aitem_giftsyo,$data;
		}elsif ($aitm_hiretu eq "ギフト"){
			push @aitem_giftda,$data;
		}else{
			push @aitem_sonota,$data;
		}
	}
	@keys0 = map {(split /<>/)[21]} @aitem_giftsyo;
	@itemgift = @aitem_giftsyo[sort {@keys0[$a] <=> @keys0[$b]} 0 .. $#keys0];
	@keys0 = map {(split /<>/)[0]} @aitem_sonota;
	@itemsonota = @aitem_sonota[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];
	@keys0 = map {(split /<>/)[21]} @aitem_giftda;
	@aitem_giftda = @aitem_giftda[sort {@keys0[$a] <=> @keys0[$b]} 0 .. $#keys0];
	@alldata = (@itemgift,@itemsonota,@aitem_giftda);
	&header(item_style);
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="gifutoya_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>ギフトに変えたいアイテムにチェックをいれ、ＯＫを押してください。交換の手数料は$koukan_money円です。<br>ＯＫの左には送りたい個数を入れることも可能\です。<br>
	※備考に（※アイコン）とある商品は、持っていることで新しいアイコンが現れます。「使用」してしまうと無くなってしまい効果も消えますのでご注意ください。<br>
	※自分で作成した「ギフト」はメール送信画面のセレクトメニューに現れます。<br>
	現在の$nameさんの身体エネルギー：$energy　頭脳エネルギー：$nou_energy</td>
	<td  bgcolor=#00bfff align=center width="200"><h1>ギフト屋</h1></td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=27><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。<br>
	</font></td></tr>
		<tr bgcolor=#00bfff><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>使用</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>売却<br>値段</td><td align=center nowrap>　備　考　</td><td align=center nowrap>購入日</td></tr>
EOM
	$now_time = time;			#ver.1.3
	@new_myitem_hairetu = ();
	$basyo = 1; #
	foreach (@alldata) {
		&syouhin_sprit($_);
#ver.1.30ここから
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){$taikyuu0 = 1;} #koko2007/04/07
		}
#ver.1.30ここまで
		if ($syo_taikyuu <= 0){$taikyuu0 = 1;} #koko2007/04/07
		$no_dis = "";

		if (!$taikyuu0){ #koko2007/04/07
			if ($maeno_syo_syubetu ne "$syo_syubetu"){
				print "<tr bgcolor=#87cefa><td colspan=27>▼$syo_syubetu</td></tr>";
			}
			if ($syo_syubetu ne "ギフト"){
				$no_dis = "<input type=radio value=\"$basyo\" name=\"basyo\">";
		
			#ver.1.3
			if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
			if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
			if ($syo_taikyuu_tani eq "日"){
				$taikyuu_hyouzi_seikei = "$nokorinissuu日";
				$baikyaku_hyouzi = ($tanka * $nokorinissuu);
			}else{
				$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
				$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
			}

#ver.1.3ここまで
			&byou_hiduke($syo_kounyuubi);
			if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
				$disp_siyukanou = "－";
				$no_dis =""; #koko2007/10/16
			}else{$disp_siyukanou = "OK";}

			}	#ギフトで無い場合閉じ 		ver.1.3
			if ($syo_syubetu eq "ギフト"){
				$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			}
			print <<"EOM";
<tr bgcolor=#b0e0e6 align=center><td nowrap align=left>$no_dis $syo_hinmoku</td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$disp_siyukanou</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$baikyaku_hyouzi円</td><td align=left>$syo_comment</td><td nowrap>$bh_tukihi</td></tr>
EOM
		}#koko2007/04/07
		$taikyuu0 = 0;#koko2007/04/07
		$maeno_syo_syubetu = "$syo_syubetu";
		&syouhin_temp;			#ver.1.3
		push (@new_myitem_hairetu,$syo_temp);			#ver.1.3
		$basyo++; #
	}		#foreach閉じ
	if (! @alldata){print "<tr><td colspan=27>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
	<tr><td colspan=27>
	<div align=center>
	<input type=\"text\" name=\"henkansu\" size=\"2\" value=\"\" maxlength=\"2\"><!--koko-->
	<input type=submit value=" O K "></div></td></tr>
	</table></form>
EOM
#自分の所有物ファイルを更新
	&lock;
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);
#koko2006/11/27
	$loop_count = 0;
	while ($loop_count <= 10){
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @new_myitem_hairetu ne ""){
		#	sleep(1);#2006/11/27#koko2007/02/02
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#kokoend
	&unlock;
	&hooter("login_view","戻る");
	exit;
}
#######アイテム変換
sub gifutoya_do {
	if ($in{'basyo'} eq ""){&error("アイテムが選ばれていません。");}
	if(!$k_id){&error("mono.cgi エラー gifutoya2")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;#koko2006/10/20
	close(OUT);
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		if ($syo_kouka =~ m/ギフト/){$syo_syubetu = "ギフト";}
		if ($syo_taikyuu <= 0){next;}
		if ($syo_syubetu eq "ギフト"){$gift_item_suu ++ ;next;}
		if ($syo_syubetu eq "ギフト商品"){$gift_mothisuu ++ ;next;}
		$my_item_suu ++ ;
	}
	if ( $gift_item_suu >= $kounyu_gift_gendo){
		&error("$gift_item_suu/$kounyu_gift_gendo 持ち物が持ちすぎに成るため変更出来ません。");
	}
	&syouhin_sprit($myitem_hairetu[$in{'basyo'} - 1]);

	if ($in{'henkansu'}){
		if ($in{'henkansu'} =~ m/\D/){
			&error("数字のみを受け付けます。");
		}
	}
#koko2006/08/26
	if ($syo_syubetu eq "食料品" && !($syo_kouka =~ /食料品/)){
		$syo_kouka .= ",食料品";
	}
	if ($syo_syubetu eq "ファーストフード" && !($syo_kouka =~ /ファ/)){
		$syo_kouka .= ",ファ";
	}
	if ($syo_kouka =~ /ギフト/){
		$syo_kouka =~ s/,ギフト//g;
		$syo_kouka =~ s/ギフト//g;
	}
	$syo_kouka =~ s/無,//g;
#kokoend2006/08/26
#koko2007/01/01
	if ($syo_taikyuu_tani eq "日"){
		$now_time = time;
		$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
		$nokorinissuu = $syo_taikyuu - $keikanissuu;
		$syo_kounyuubi = $now_time;
		$syo_taikyuu = $nokorinissuu;
	}
#kokoend
	if ($in{'henkansu'} <= 0 || $in{'henkansu'} >= $syo_taikyuu){
		$syo_syubetu = "ギフト";
		
		$money -= $koukan_money;
		&syouhin_temp;
		$myitem_hairetu[$in{'basyo'} - 1] = $syo_temp;
	}else{
		$syo_taikyuu -= $in{'henkansu'};
		$money -= $koukan_money;
		&syouhin_temp;
		$myitem_hairetu[$in{'basyo'} - 1] = $syo_temp;
		$syo_syubetu = "ギフト";
		$syo_taikyuu = $in{'henkansu'};
		&syouhin_temp;
		push (@myitem_hairetu,$syo_temp);
	}

	if(!$k_id){&error("mono.cgi エラー gifutoya3")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";

	&lock; #koko2006/10/20
	open(OUT,">$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); }; #koko2006/10/20
	print OUT @myitem_hairetu;
	close(OUT);
#koko2006/11/27
	$loop_count = 0;
	while ($loop_count <= 10){
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @myitem_hairetu ne ""){
		#	sleep(1);#2006/11/27#koko2007/02/02
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#kokoend
	&unlock;

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&gifutoya;
}
