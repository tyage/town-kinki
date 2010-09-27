#!/usr/bin/perl

##########################
# データーファィル名
$otakara_dat_fail = "./dat_dir/otakara.cgi";
# ログファイル名
$otakara_logfile = './log_dir/otakara_log.cgi';
# 持ち金制限 'yes'
$motiganeseigen = 'yes';
# 連続可能か
$ota_rentou = 'yes';
# ゲーム間隔(分)
$otakara_game_time = 5;
# 銅金額
$mane_dou = 500;
# 銀金額
$mane_gin = 1000;
# 金金額
$mane_kin = 2500000;
# スペシャル金額
$mane_sp = 500000;
##########################

$this_script = 'otakara.cgi';
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

# 使用時間の保持
	if($in{'mode'} eq "otakara"){&otakara;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub otakara{
	$comment = "";
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("Open Error : $monokiroku_file");
	@my_item_list = <OUT>;
	close(OUT);
	foreach (@my_item_list){
		&syouhin_sprit($_);
#所属変更　ギフト・食料品 #koko2006/08/24
		if ($syo_kouka =~ m/ギフト/){$syo_syubetu = "ギフト";}
#kokoend2006/08/24
		if ($syo_taikyuu <= 0){next;}
		if ($syo_syubetu eq "ギフト"){$gift_item_suu ++ ;next;}
		if ($syo_syubetu eq "ギフト商品"){$gift_mothisuu ++ ;next;}
		$my_item_suu ++ ;
	}

	if ($my_item_suu >= $syoyuu_gendosuu ||$gift_mothisuu >= $gift_gendo +1 || $gift_item_suu >= $kounyu_gift_gendo){
		if ($my_item_suu eq ""){$my_item_suu = 0;}
		if ($gift_mothisuu eq ""){$gift_mothisuu = 0;}
		if ($gift_gendo eq ""){$gift_gendo = 0;}
		&error("$my_item_suu/$syoyuu_gendosuu,$gift_mothisuu/$gift_gendo,$gift_item_suu/$kounyu_gift_gendo 持ち物が持ちすぎに成るため引けません。","yes");
	}

	if ($motiganeseigen eq 'yes'){
		if ($mane_sp <= $money){
			$hikeruka0 = "<input type=submit  name=takara value=\"スペシャル\">\n";
		}
		if ($mane_kin <= $money){
			$hikeruka1 = "<input type=submit  name=takara value=\"金の箱\">\n";
		}
		if ($mane_gin <= $money){
			$hikeruka2 = "<input type=submit  name=takara value=\"銀の箱\">\n";
		}
		if ($mane_dou <= $money){
			$hikeruka3 = "<input type=submit  name=takara value=\"銅の箱\">\n";;
		}
	}else{
		$hikeruka0 = "<input type=submit  name=takara value=\"スペシャル\">\n";
		$hikeruka1 = "<input type=submit  name=takara value=\"金の箱\">\n";
		$hikeruka2 = "<input type=submit  name=takara value=\"銀の箱\">\n";
		$hikeruka3 = "<input type=submit  name=takara value=\"銅の箱\">\n";
	}

	if ($hikeruka0 eq "" && $hikeruka1 eq "" && $hikeruka2 eq "" && $hikeruka3 eq ""){
		$hikeruka = "持ち金が足りなくて引けません。\n";
	}

	if ($tajuukinsi_flag==1){&tajuucheck;}
	open(MA,"$otakara_logfile") || &error("$otakara_logfileが開けません");
	@otakara_dat = <MA>;
	close(MA);
	($ota_name,$ota_time,$ota_hako,$ota_item)= split(/<>/,$otakara_dat[0]);

#引くコマンドだった場合
	if ($in{'command'} eq "hiku"){
		$now_time = time ;
		if ($name eq $ota_name && $ota_rentou ne 'yes'){&error("同じ方が続けてお宝を引くことはできません");}
		foreach (@otakara_dat){
			($ota_name,$ota_time,$ota_hako,$ota_item)= split(/<>/);
				if ($name eq $ota_name){
					if ($now_time - $ota_time < 60*$otakara_game_time){&error("最後にゲームしてからまだ$otakara_game_time分すぎていません。");}
				}
		}

		open(OT,"$otakara_dat_fail") || &error("$otakara_dat_failが開けません");
		$delmesegi = <OT>;
		@takaramono = <OT>;
		close(OT);

		if ($in{'takara'} eq 'スペシャル'){
			$comment = 'スペシャルで';
			$otakara_money = $mane_sp;
			$takara_bangou = int(rand($#takaramono));
			$takara =$takaramono[$takara_bangou];
		} elsif ($in{'takara'} eq '金の箱'){
			$comment = '金の箱で';
			$otakara_money = $mane_kin;
			foreach $takra_tmp (@takaramono){
				&syouhin_sprit($takra_tmp);
				if ($syo_syubetu eq '金の箱'){
					push (@kin_takaramono,$takra_tmp);
				}
			}
			$takara_bangou = int(rand($#kin_takaramono));
		#	$takara_bangou = 0;#test
			$takara =$kin_takaramono[$takara_bangou];
		} elsif ($in{'takara'} eq '銀の箱'){
			$comment = '銀の箱<br>';
			$otakara_money = $mane_gin;
			foreach $takra_tmp (@takaramono){
				&syouhin_sprit($takra_tmp);
				if ($syo_syubetu eq '銀の箱'){
					push (@gin_takaramono,$takra_tmp);
				}
			}
			$takara_bangou = int(rand($#gin_takaramono));
			$takara =$gin_takaramono[$takara_bangou];
		} elsif ($in{'takara'} eq '銅の箱'){
			$comment = '銅の箱<br>';
			$otakara_money = $mane_dou;
			foreach $takra_tmp (@takaramono){
				&syouhin_sprit($takra_tmp);
				if ($syo_syubetu eq '銅の箱'){
					push (@dou_takaramono,$takra_tmp);
				}
			}
			$takara_bangou = int(rand($#dou_takaramono));
			$takara =$dou_takaramono[$takara_bangou];
		}else{$comment = "該当無し<br>";}

		&syouhin_sprit($takara);
		$get_syohin = $syo_hinmoku;
		if ($syo_kouka ne "無" && !($syo_kouka =~ m/ギフト/) && !($syo_kouka =~ m/食料品/) && !($syo_kouka =~ m/ファ/)){ #koko2006/08/24
			&takara_sutetasu;
			$comment .= "ステータスアイテム<br>$print_messe<br>";
		} else {
			&buy_otakara;
		}
			$comment .= "<div class=mainasu>$get_syohin</div>";
		$next_temp = "$name<>$now_time<>$in{'takara'}<>$get_syohin<>\n";#ここは変える事
		unshift @otakara_dat,$next_temp;
		if ($#otakara_dat +1 >= 20){$#otakara_dat =19;}
#データ更新
		open(KB,">$otakara_logfile")|| &error("Open Error : $otakara_logfile");
		eval{ flock (KB, 2); };
		print KB @otakara_dat;
		close(KB);
	}	#引く場合の閉じ

	if ($comment eq ""){$comment = "<br><br><br>\n";}


	&header(gym_style);
			print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●ルール説明<br>
	・参加者がすることは挑戦する箱を選び良いお宝を得ることです。<br>※ゲーム間隔は$otakara_game_time分です。</td>
	<td  bgcolor=#333333 align=center width=35%>
	<font color="#ffffff" size="5"><b>お宝</b></font>
	</td>
	</tr></table><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr><td>
	<div align=center>
	<!-- $otakara_dis<br> -->
	$money円
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="otakara">
	<input type=hidden name=command value="hiku">
	<input type=hidden name=mysec value="$in{'mysec'}"><!-- koko2006/04/01 -->
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=gamerand value="$in{'gamerand'}">
	$hikeruka0 $hikeruka1 $hikeruka2 $hikeruka3
	$hikeruka
	</form>
	</div>
EOM

	print <<"EOM";
	</td><td width=100% valign=top>
	<table  border="0" cellspacing="0" cellpadding="10" width=100% height=100% bgcolor=#66cc33 style="border: #663300; border-style: solid; border-width: 2px;">
<tr><td>$comment</td></tr>
		</table>
	</td></tr></table>
	
<br><table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
	<div class=honbun2>■最近のお宝ゲット</div>
EOM
	foreach (@otakara_dat){
		($ota_name,$ota_time,$ota_hako,$ota_item)= split(/<>/);
		print "$ota_nameさんが$ota_hakoに挑戦して$ota_itemを得ました。<br>\n";
	}
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;

}
	
#############以下サブルーチン

####購入処理
sub buy_otakara {
#	($katta_syouhin,$katta_taikyuu,$katta_nedan,$katta_syubetu) = split(/,&,/,$in{'syo_hinmoku'});

	$katta_syouhin = $get_syohin;
	$katta_taikyuu = $syo_taikyuu;
	$katta_nedan = $syo_nedan;
	$katta_syubetu = $syo_syubetu;
	$katta_syubetu_b = $syo_syubetu;#koko2006/08/24
	@kounyuu_hairetu = @takaramono;

#自分の購入物ファイルにその商品があるかチェック
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	@my_item_list = <OUT>;
	close(OUT);

	$my_item_suu = 0;
	$gift_item_suu = 0;

	foreach (@my_item_list){
		&syouhin_sprit($_);
#koko2006/08/24
# 注意　「ファースト」などの「ー」がマッチングでエラーになる。
		$katta_syubetu = $katta_syubetu_b; #koko2006/08/24 戻し
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
		if ($syo_taikyuu <= 0){next;}
		if ($syo_syubetu eq "ギフト"){$gift_item_suu ++ ;next;}
		if ($syo_syubetu eq "ギフト商品"){next;}
		$my_item_suu ++ ;
	}

	foreach (@my_item_list){
		&syouhin_sprit($_);
#持っていた場合
		if ($katta_syouhin eq "$syo_hinmoku" && $syo_syubetu ne "ギフト商品" && $syo_syubetu ne "ギフト" && $katta_syubetu eq $syo_syubetu){

			if ($my_item_suu >= $syoyuu_gendosuu){&error("これ以上所有できません。持ち物の所有限度数は$syoyuu_gendosuuです。");}
			
			if ($syo_taikyuu_tani eq "回" || $syo_taikyuu_tani eq "日"){ #koko 最初の回は出ない。
				$nokotteru_taikyuu = $syo_taikyuu;
				$syo_taikyuu += $katta_taikyuu;
				if ($syo_taikyuu > $katta_taikyuu*$item_kosuuseigen){&error("これ以上このアイテムを増やすことはできません。");}
				if ($cashback_flag eq "on"){
					$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan - $cashback_kingaku) / $syo_taikyuu);
				}else{
					$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan) / $syo_taikyuu);
				}
				$motteru_flag =1;
				$kounyuu_ok = 1;
			}
#ver.1.30ここまで
		}
		&syouhin_temp;
		push (@new_myitem_list,$syo_temp);
	}		#foreachの閉じ
	
#持っていなかった場合
	if ($motteru_flag ==0){
		if ($my_item_suu >= $syoyuu_gendosuu){&error("これ以上所有できません。持ち物の所有限度数は$syoyuu_gendosuuです。");}
		if ($gift_item_suu >= $kounyu_gift_gendo){&error("これ以上所有できません。ギフトの購入限度数$kounyu_gift_gendoに達しています。");}

		$kounyuu_ok = 0;

		foreach (@kounyuu_hairetu){
			&syouhin_sprit($_);
#koko2006/08/24
			if ($syo_kouka =~ m/ギフト/){
				$syo_syubetu = "ギフト";
			}
			if ($syo_kouka =~ m/食料品/){
				$syo_syubetu = "食料品";
			}
			if ($syo_kouka =~ m/ファ/){
				$syo_syubetu = "ファーストフード";
			}
#kokoend2006/08/2ファーストフード
			if ($katta_syouhin eq "$syo_hinmoku"){
#購入日を記録
				$syo_kounyuubi = time;
#ver.1.30ここから
				if ($cashback_flag eq "on"){
					$tanka = int (($katta_nedan - $cashback_kingaku) / $syo_taikyuu);
				}else{
					$tanka = int ($katta_nedan / $syo_taikyuu);
				}
				&syouhin_temp;
				push (@new_myitem_list,$syo_temp);
#ver.1.30ここまで
				$kounyuu_ok = 1;
				last;
			}
		}
	}		#持っていなかった場合の閉じ
	if ($kounyuu_ok == 0){&error("$katta_syouhinをゲットできませんでした。");}

#自分の購入物ファイルのログ更新
	&lock;

	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,">$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_list;
	close(OUT);
#koko2006/11/27
	$loop_count = 0;
	while ($loop_count <= 10){
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

	&unlock;
	
#ログ更新
	$money -= $otakara_money;
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	return;
}
############################
sub takara_sutetasu{
	$now_time = time;
	if ($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード"){
		if($now_time < $last_syokuzi + ($syokuzi_kankaku*60)){
			$sinamono_min = int(($last_syokuzi + $syokuzi_kankaku*60 - $now_time) / 60);
			$sinamono_sec = ($last_syokuzi + $syokuzi_kankaku*60 - $now_time) % 60;
			&error("まだ食事できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
		}
		$last_syokuzi = $now_time;
	}
	if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
		$sinamono_min = int(($syo_siyou_date + ($syo_kankaku*60) -$now_time) / 60);
		$sinamono_sec = ($syo_siyou_date + ($syo_kankaku*60) -$now_time) % 60;
		&error("間隔が短いためまだ使用できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
	}

	if($energy < $syo_sintai_syouhi){&error("身体パワーが足りません。");}
	if($nou_energy < $syo_zunou_syouhi){&error("頭脳パワーが足りません。");}
	if($syo_kokugo){$kokugo += $syo_kokugo; $print_messe .= "・国語が$syo_kokugoアップしました。<br>";}
	if($syo_suugaku){$suugaku += $syo_suugaku; $print_messe .= "・数学が$syo_suugakuアップしました。<br>";}
	if($syo_rika){$rika += $syo_rika; $print_messe .= "・理科が$syo_rikaアップしました。<br>";}
	if($syo_syakai){$syakai += $syo_syakai; $print_messe .= "・社会が$syo_syakaiアップしました。<br>";}
	if($syo_eigo){$eigo += $syo_eigo; $print_messe .= "・英語が$syo_eigoアップしました。<br>";}
	if($syo_ongaku){$ongaku += $syo_ongaku; $print_messe .= "・音楽が$syo_ongakuアップしました。<br>";}
	if($syo_bijutu){$bijutu += $syo_bijutu; $print_messe .= "・美術が$syo_bijutuアップしました。<br>";}
	if($syo_looks){$looks += $syo_looks; $print_messe .= "・ルックス値が$syo_looksアップしました。<br>";}
	if($syo_tairyoku){$tairyoku += $syo_tairyoku; $print_messe .= "・体力が$syo_tairyokuアップしました。<br>";}
	if($syo_kenkou){$kenkou += $syo_kenkou; $print_messe .= "・健康値が$syo_kenkouアップしました。<br>";}
	if($syo_speed){$speed += $syo_speed; $print_messe .= "・スピードが$syo_speedアップしました。<br>";}
	if($syo_power){$power += $syo_power; $print_messe .= "・パワーが$syo_powerアップしました。<br>";}
	if($syo_wanryoku){$wanryoku += $syo_wanryoku; $print_messe .= "・腕力が$syo_wanryokuアップしました。<br>";}
	if($syo_kyakuryoku){$kyakuryoku += $syo_kyakuryoku; $print_messe .= "・脚力が$syo_kyakuryokuアップしました。<br>";}
	if($syo_love){$love += $syo_love; $print_messe .= "・LOVE度が$syo_loveアップしました。<br>";}
	if($syo_unique){$unique += $syo_unique; $print_messe .= "・面白さが$syo_uniqueアップしました。<br>";}
	if($syo_etti){$etti += $syo_etti; $print_messe .= "・エッチ度が$syo_ettiアップしました。<br>";}
#効果の設定
#koko2006/09/22
	if ($print_messe eq ""){
		$money += $syo_nedan;
		if ($syo_nedan =~ /^[-+]?\d\d\d\d+/g) {
			for ($i = pos($syo_nedan) - 3, $j = $syo_nedan =~ /^[-+]/; $i > $j; $i -= 3){substr($syo_nedan, $i, 0) = ',';}
		}
		$print_messe .= "・お金が$syo_nedan円当たりました。<br>";
	}
#kokoend
	if($syo_kouka ne "無"){
		($koukahadou,$sonoiryoku) = split(/,/,$syo_kouka);
		if ($koukahadou eq "万能\"){
			$byouki_sisuu += $sonoiryoku;
		}
		if ($koukahadou eq "風邪"){
			if ($byoumei =~ /風邪/){$byouki_sisuu += $sonoiryoku;}
		}
		if ($koukahadou eq "下痢"){
			if ($byoumei =~ /下痢/){$byouki_sisuu += $sonoiryoku;}
		}
		if ($koukahadou eq "肺炎"){
			if ($byoumei =~ /肺炎/){$byouki_sisuu += $sonoiryoku;}
		}
		if ($koukahadou eq "結核"){
			if ($byoumei =~ /結核/){$byouki_sisuu += $sonoiryoku;}
		}
		if ($koukahadou eq "ウエイトアップ"){
			$taijuu += $sonoiryoku;
			$print_messe .= "・体重が$sonoiryoku kg増えました。<br>";
		}
		if ($koukahadou eq "ダイエット"){
			$taijuu -= $sonoiryoku;
			$print_messe .= "・体重が$sonoiryoku kg減りました。<br>";
		}
		if ($koukahadou eq "身長"){
			$sintyou += $sonoiryoku;
			$print_messe .= "・身長が$sonoiryoku cm伸びました。<br>";
		}
		if ($koukahadou eq "縮み"){
			$sintyou -= $sonoiryoku;
			$print_messe .= "・身長が$sonoiryoku cm縮みました。<br>";
		}
	}

	$syo_siyou_date = $now_time;
	if($syo_sintai_syouhi){$energy -= $syo_sintai_syouhi;$print_messe .= "・$syo_sintai_syouhiの身体エネルギーを使いました。<br>";}
	if($syo_zunou_syouhi){$nou_energy -= $syo_zunou_syouhi;$print_messe .= "・$syo_zunou_syouhiの頭脳エネルギーを使いました。<br>";}
	if($syo_cal){
		$taijuu_hue = $syo_cal / 1000;
		$taijuu += $taijuu_hue; $print_messe .= "・$taijuu_hue kg体重が増えました。<br>";
	}
#自分の所有物ファイルを更新
	$money -= $otakara_money;
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	return;
}
