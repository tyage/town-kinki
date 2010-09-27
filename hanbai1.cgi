#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
##############################################
# 販売品目のログファイル
$hanbai1_logfile ='./log_dir/hanbai1_log.cgi';
# 販売商品の入ったデータファイル
$hanbai1_detafile = './dat_dir/syouhin.cgi';#'./dat_dir/syoten.cgi'
# 自動更新する時間
$habaikoushin = 1;
# お店の販売品目の種別
$hanbai_hinmoku = '餌';
##############################################

$this_script = 'hanbai1.cgi';
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
	if($in{'mode'} eq "hanbai1"){&hanbai1;}
	if($in{'mode'} eq 'buy_syouhin_1'){&buy_syouhin_1;}
#	elsif($in{'mode'} eq "kyushitu_go"){&kyushitu_go;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

#sub unit_pl{
########################################################################
# unit.pl
#"販売1" => "<form method=POST action=\"hanbai1.cgi\"><input type=hidden name=mode value=\"hanbai1\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/house1.gif'  onMouseOver='onMes5(\"お店1\")' onMouseOut='onMes5(\"\")'></td></form>",
########################################################################
#}
#############  #############

sub hanbai1{
#koko2007/08/15
#kokoend
	open(IN,"$hanbai1_logfile") || &error("Open Error : $hanbai_logfile");
	eval{ flock (IN, 2); };
	$hanbai_kanri = <IN>;
	@syokudou_hairetu = <IN>;
	close(IN);
	($hanbai_furag)=split(/<>/, $hanbai_kanri);
	my($sec,$min,$hour,$mday,$mon,$year) = localtime (time);
	if(($habaikoushin <= $hour && $hanbai_furag == 0) || $in{'sudoukoushin'} eq "yes"){##
		open(OL,"$hanbai1_detafile") || &error("Open Error : $hanbai_detafile");
		eval{ flock (OL, 2); };
		$hanbai_icigyo = <OL>;
		@new_syouhin_hairetu = ();
	#	while (<OL>){
	#		my $r = rand @new_syouhin_hairetu+1;
	#		push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
	#		$new_syouhin_hairetu[$r] = $_;
	#	}
		@new_syouhin_hairetu = <OL>;
		close(OL);
	#	$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu eq "食"){next;}
#koko2006/11/21
			if ($hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/){next;}
#kokoend
		#	$syo_zaiko = int($syo_zaiko/$zaiko_tyousetuti);
		#	if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			if($syo_syubetu eq $hanbai_hinmoku){
				&syouhin_temp;
				push (@new_syouhin_hairetu2,$syo_temp);
		#		$i ++;
		#		if ($i >= $habaisurukazu){last;}
			}
		}
		@alldata = @new_syouhin_hairetu2;
		@keys0 = map {(split /<>/)[0]} @alldata;
		@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];
		open(OLOUT,">$hanbai1_logfile") || &error("$hanbai1_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT "1<>$hour<>\n";
		print OLOUT @alldata;
		close(OLOUT);
		@syokudou_hairetu = @alldata;
	}elsif ($habaikoushin > $hour && $hanbai_furag == 1){###
		open(OLOUT,">$hanbai1_logfile") || &error("$hanbai1_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT "0<>$hour<>\n";
		print OLOUT @syokudou_hairetu;
		close(OLOUT);
	}

	&header(syokudou_style);
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="buy_syouhin_1">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>自動販売機です。品揃えは毎日変わります。一度に持てる所有物の限度は$syoyuu_gendosuu品目です。<div class="honbun2">●$nameさんの所持金：$money円</div></td>
	<td  bgcolor=#333333 align=center>自動販売機</td>
	</tr></table><br>
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br></font>
	<font color=#ff6600>※ギフトは贈り物専用の商品です。自分で使用することはできません。</font></td></tr>
EOM
	foreach (@syokudou_hairetu) {
		&syouhin_sprit($_);
		if($syo_zaiko <= 0){
			$kounyuubotan ="";
			$syo_zaiko = "売り切れ";
		}else{
			$kounyuubotan ="<input type=radio value=\"$syo_hinmoku,&,$syo_taikyuu,&,$syo_nedan,&,$syo_syubetu,&,\" name=\"syo_hinmoku\">"; #koko2006/08/22
		}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "ー";}
		if ($maeno_syo_syubetu ne "$syo_syubetu"){
		print <<"EOM";
		<tr bgcolor=#ff9933><td align=center nowrap>商品</td><td align=center nowrap>在庫</td><td align=center>価格</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center nowrap>耐久</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td></tr><!-- #koko2006/11/08 -->
				<tr bgcolor=#ffff66><td colspan=26>▼$syo_syubetu</td></tr>
EOM
		}
		$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
#ver.1.3ここから
		if ($syo_nedan =~ /^[-+]?\d\d\d\d+/g) {
			for ($i = pos($syo_nedan) - 3, $j = $syo_nedan =~ /^[-+]/; $i > $j; $i -= 3) {
  				substr($syo_nedan, $i, 0) = ',';
 			 }
		}
#ver.1.3ここまで
#koko2006/11/08
	if ($syo_comment){
		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=24>【 備考 】 $syo_comment</td></tr>";
	}else{
		$disp_seru = "";
		$disp_com = "";
	}
		print <<"EOM";
<tr bgcolor=#ffcc66 align=center><td width=150 align=left $disp_seru>$kounyuubotan $syo_hinmoku</td><td align=right>$syo_zaiko</td><td align=right nowrap>$syo_nedan円</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
#kokoend
		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
#ver.1.30ここから
#所有物チェック　koko2007/08/15 場所変更
#	$monokiroku_file="./member/$k_id/mono.cgi";
#	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
#	eval{ flock (OUT, 2); };
#	@my_kounyuu_list =<OUT>;
#	close(OUT); #kokoend
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
	}
	print <<"EOM";
	<tr><td colspan=26><div align=center>
	支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
	　<input type=submit value=" O K "></div></td></tr>
	</table></form>
EOM
#ver1.30ここまで
	if ($in{'name'} eq $admin_name){
		print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="hanbai1">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=sudoukoushin value="yes">
	<input type=submit value="手動更新">
	</form>
EOM
	}
	&hooter("login_view","戻る");
	exit;

}
#kokoend
####購入処理
sub buy_syouhin_1 {
#ver.1.30ここから
	($katta_syouhin,$katta_taikyuu,$katta_nedan,$katta_syubetu) = split(/,&,/,$in{'syo_hinmoku'});#koko2006/08/22 $syo_syubetu
	$katta_syubetu_b = $katta_syubetu;#koko2006/08/23

	if ($in{'siharaihouhou'} eq "現金"){
		if ($katta_nedan > $money){&error("お金が足りません");}
	}

#自分の購入物ファイルにその商品があるかチェック
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_item_list = <OUT>;
	close(OUT);

	$gift_item_suu = 0;#koko2006/08/21 #koko2006/08/28 場所移動
	$my_item_suu = 0;#koko2006/08/21

	foreach (@my_item_list){
		&syouhin_sprit($_);
#所属変更　ギフト・食料品 #koko2006/08/23
		if ($syo_kouka =~ m/ギフト/){$syo_syubetu = "ギフト";}
#kokoend2006/08/23
		if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;} #koko2006/11/14)
		if ($syo_syubetu eq "ギフト"){
#koko2006/10/12
			if ($katta_syouhin eq $syo_hinmoku){
				$item_gift_chc = 1;
			}
#kokoend
			$gift_item_suu ++ ;
			next;
		}
		if ($syo_syubetu eq "ギフト商品"){next;}
		if (!($syo_taikyuu <= 0)){ #koko2006/11/14
			$my_item_suu ++ ;
		} #kokoend
	}
	$katta_syouhin_tmp = $katta_syouhin;
	if ($katta_syouhin eq '子猫'){$katta_syouhin = "$in{'name'}の子猫";}

	$motteru_flag =0;
	@new_myitem_list = (); #koko2007/06/05
	foreach (@my_item_list){
		&syouhin_sprit($_);
#持っていた場合
#koko2006/08/23
		$katta_syubetu = $katta_syubetu_b; #koko2006/08/23 戻し
		if ($syo_kouka =~ m/ギフト/){
			$syo_syubetu = "ギフト";
		}
		if ($syo_kouka =~ m/食料品/){
			$syo_syubetu = "食料品";
			$katta_syubetu = $syo_syubetu;
		}
		if ($syo_kouka =~ m/ファ/){
			$syo_syubetu = "ファーストフード";
			$katta_syubetu = $syo_syubetu;
		}

#kokoend2006/08/23
		if ($katta_syouhin eq "$syo_hinmoku" && $syo_syubetu ne "ギフト商品" && $syo_syubetu ne "ギフト" && $katta_syubetu eq "$syo_syubetu"){
#koko2006/08/22
		#	if ($my_item_suu >= $syoyuu_gendosuu && !$item_moteru){&error("これ以上所有できません。持ち物の所有限度数は$my_item_suu/$syoyuu_gendosuu ギフトの購入限度数$gift_item_suu/$kounyu_gift_gendoに達しています1。");} #koko2006/10/12
			if ($syo_taikyuu_tani eq "回" || $syo_taikyuu_tani eq "日"){ #koko 最初の回は出ない。
				$nokotteru_taikyuu = $syo_taikyuu;
				$syo_taikyuu += $katta_taikyuu;
#koko 2005/04/18
				$motikosuu = int($syo_taikyuu / $katta_taikyuu);
				if ($syo_taikyuu % $katta_taikyuu > 0){$motikosuu++;}
#kokoend
				if ($syo_taikyuu > $katta_taikyuu*$item_kosuuseigen){&error("これ以上このアイテムを増やすことはできません。");}		#ver.1.2
				if ($cashback_flag eq "on"){
					$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan - $cashback_kingaku) / $syo_taikyuu);
				}else{
					$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan) / $syo_taikyuu);
				}
				$motteru_flag =1;
			}
			if ($in{'siharaihouhou'} ne "現金"){
				if($bank - $katta_nedan < 0){&error("貯金がありません。");} #2007/03/19
				$bank -= $katta_nedan;
				&kityou_syori("クレジット支払い（$katta_syouhin）","$katta_nedan","",$bank,"普");
			}else{
				$money -= $katta_nedan;
			}
#ver.1.30ここまで
		}
		&syouhin_temp;
		push (@new_myitem_list,$syo_temp);
	}		#foreachの閉じ
#koko2006/10/22
	$katta_syouhin = $katta_syouhin_tmp;
#kokoend

#持っていなかった場合
	if ($motteru_flag == 0){
#koko2006/10/12
		if ($my_item_suu >= $syoyuu_gendosuu && $gift_item_suu >= $kounyu_gift_gendo){
			&error("これ以上所有できません。持ち物の所有限度数は$my_item_suu/$syoyuu_gendosuu ギフトの購入限度数$gift_item_suu/$kounyu_gift_gendoに達しています2。");
		}
		if (!($my_item_suu >= $syoyuu_gendosuu) && $item_gift_chc && $gift_item_suu >= $kounyu_gift_gendo){
			&error("これ以上所有できません。ギフトの購入限度数$gift_item_suu/$kounyu_gift_gendoに達しています3。");
		}
		if (!($gift_item_suu >= $kounyu_gift_gendo) && !$item_gift_chc && $my_item_suu >= $syoyuu_gendosuu){
			&error("これ以上所有できません。持ち物の所有限度数は$my_item_suu/$syoyuu_gendosuuに達しています4。");
		}
#kokoend
	#	}elsif($departset == 3){
		open(KOM,"$hanbai1_logfile") || &error("Open Error : $hanbai_logfile");
		eval{ flock (KOM, 2); };
		$hanbai_kanri = <KOM>;
		@kounyuu_hairetu = <KOM>;
		close(KOM);
#koko2006/11/20
	#	}else{
		$kounyuu_ok = 0;
		foreach (@kounyuu_hairetu){
			&syouhin_sprit($_);
#koko2006/08/23
			if ($syo_kouka =~ m/ギフト/){
				$syo_syubetu = "ギフト";
			}
			if ($syo_kouka =~ m/食料品/){
				$syo_syubetu = "食料品";
			}
			if ($syo_kouka =~ m/ファ/){
				$syo_syubetu = "ファーストフード";
			}
#kokoend2006/08/23ファーストフード
			if ($katta_syouhin eq "$syo_hinmoku"){		
#ver.1.3
				$oboe_syubetu = $syo_syubetu;#koko2006/04/10
#購入日を記録
				$syo_kounyuubi = time;
#ver.1.30ここから
				if ($cashback_flag eq "on"){
					$tanka = int (($katta_nedan - $cashback_kingaku) / $syo_taikyuu);
				}else{
					$tanka = int ($katta_nedan / $syo_taikyuu);
				}
#koko2006/10/22
				if ($syo_hinmoku eq '子猫'){$syo_hinmoku = "$in{'name'}の子猫";}

#kokoend
				&syouhin_temp;
				push (@new_myitem_list,$syo_temp);
				if ($in{'siharaihouhou'} ne "現金"){
				if($bank - $katta_nedan < 0){&error("貯金がありません。");} #2007/03/19
					$bank -= $katta_nedan;
					&kityou_syori("クレジット支払い（$katta_syouhin）","$katta_nedan","",$bank,"普");
				}else{
					$money -= $katta_nedan;
				}
#ver.1.30ここまで
				$kounyuu_ok = 1;
				last;
			}
		}
		if ($kounyuu_ok == 0){&error("$katta_syouhin購入できませんでした。");}
	}		#持っていなかった場合の閉じ
#	&lock;
	
#個人のお店なら在庫を引いてお金を入金＆記帳
#ver.1.30ここから
#街の経済力アップ
	#	}elsif ($departset == 3){
	open(SYO,"$hanbai1_logfile") || &error("Open Error : $hanbai1_logfile");
	eval{ flock (SYO, 2); };
	$hanbai_kanri = <SYO>;
	@depa_zan = <SYO>;
	close(SYO);
#kokoend2006/11/28
	#	}else{
	@new_depa_zan=();
	$syo_atta_fg=0;		#ver.1.22
	foreach (@depa_zan){
		&syouhin_sprit($_);
		if($katta_syouhin eq "$syo_hinmoku"){
			if ($syo_zaiko <= 0){&error("在庫切れです");}	#ver1.2
			$syo_zaiko = $syo_zaiko-1 ;
			$syo_atta_fg=1;		#ver.1.22
		}
		if ($syo_zaiko <= 0){next;}
		&syouhin_temp;
		push (@new_depa_zan,$syo_temp);
	}
	if($syo_atta_fg==0){&error("在庫がありません。");};		#ver.1.22
	#	}elsif($departset == 3){

	open(OLOUT,">$hanbai1_logfile") || &error("Open Error : $hanbai1_logfile");
	eval{ flock (OLOUT, 2); };
	print OLOUT $hanbai_kanri;
	print OLOUT @new_depa_zan;;
	close(OLOUT);
#	}
#ver1.22
#自分の購入物ファイルのログ更新
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,">$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_list;
	close(OUT);
#koko2006/11/02
	$loop_count = 0;
	while ($loop_count <= 10){
		for (0..100){$i=0;}
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @new_myitem_list ne ""){
		#	sleep(1);#2006/11/27#koko2007/02/02
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_list;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
#kokoend

#	&unlock;
	
#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	&header("","sonomati");
#koko2006/04/10
	if (!$motikosuu && $oboe_syubetu eq "ギフト"){
		$gift_item_suu++;
		$motikosuu = 0;
	}elsif(!$motikosuu){
		$motikosuu = 1;
		$my_item_suu++;
	} #koko2005/04/18
#kokoend2006/04/10
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$katta_syouhinを購入しました。<br>ギフトは$gift_item_suu個です。$cashback_message<br>現在のアイテム所持数は $my_item_suu個です。$motikosuuセットあります。<!-- koko 2005/04/18 -->
</span>
</td></tr></table>
<br>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>

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

