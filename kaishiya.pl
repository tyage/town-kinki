# 運営処理　2007/05/05 パラ減量　2008/08/18

# 運営間隔 時間1
$unei_time =1;
# 運営効率
$unei_koritu = 10;
# 総合指数　身長

# 社員教育費
$kyouikuhiyou = 20000;

$unei_yobi5s = "170.0"; #Cm
# 総合指数　体重
$unei_yobi6s = "65.0"; #Kg

# 社員上限  #koko2007/05/05
$syain_tantou = 3;
# 役員上限　#koko2007/05/05
$yakuin_jougen = 10;

# 社員が減った時に下のパラメーターを消す。'yes'
$syinsyoukyo = 'no';
###################################################
sub kaishiya {
#	呼び出し前に  # ($in{'ori_ie_id'},$bangou)が行われている。
	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."$bangou";
	($kaisya_id,$bangou) = split(/_/,$in{'ori_ie_id'});
	$unei_file="./member/$kaisya_id/$bangou"."_log.cgi"; #koko2007/04/21

	open(UNEI,"< $unei_file") || &error("Open Error : $unei_file");
	eval{ flock (UNEI, 1); };
	@all_unei = <UNEI>;
	close(UNEI);

	open (KAISYA,"< ./member/$kaisya_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_bbs.cgi");
	eval{ flock (KAISYA, 1); };
	$kanri_bbs = <KAISYA>;
	@kiji_bbs = <KAISYA>;
	close(KAISYA);

	($opn_no,$men_no,$kai0_id,$kai_name_kanre,$kaitime,$kakikomijikan,$yomidashijikan) = split(/<>/,$kanri_bbs); #koko2007/05/29
	chomp $kakikomijikan;
	chomp $yomidashijikan;

#		$sodate_taisyou_flg=0; #メモ書き
#		foreach (@all_kodomo){
#			if ($unei_num eq $bangou){}
#		}

	($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank,$unei_syoku)=split(/<>/, $all_unei[0]);
	chomp $unei_syoku;
#koko2008/08/18
	$now_time = time;
#	(@times) = localtime;
	
#	if($unei_oya1+1*24*60*60 < $now_time && $times[6] == 1){ #月曜日
#		$genryou = 1;
#		$unei_oya1 = $now_time;
#	}
#end8/18
	if (!$ori_ie_rank){return;}

	open (KAISYA,"< ./member/$kaisya_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_kanri.cgi");
	eval{ flock (KAISYA, 1); };
	@yakuin_list = <KAISYA>;
	close(KAISYA);

	$menba = "";
	foreach (@yakuin_list){
		($kai_id,$kai_name,$kai_time) = split(/<>/);
		if ($in{'name'} eq $kai_name){
			$menba = $kai_name;
		}
		$menba_list .= "$kai_name,";
		$sankakyohi .= "<input type=radio name=taikai value=\"out\">$kai_name \n"
	}

	if($yakuin_jougen < $#yakuin_list + 1){$#yakuin_list = $yakuin_jougen-1;}

	$syainjougen = $syain_tantou * ($#yakuin_list + 1);

	if ($in{'command'} eq 'kaisya_bbs'){&kaisya_bbs;}
	if ($in{'command'} eq 'syain_up'){
		push @all_unei,"$unei_num<>$unei_name<><><><>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<><><><>0<>$unei_yobi5<>$unei_yobi6<><>0<><>$ori_ie_rank<>\n";
	}

	$i=0;
	@new_uneiomo_temp = (); #$koko2007/06/05
	
	#改造しました
	if($in{'command'} eq "do_unei2"){
		foreach (@all_unei){
			($unei_num,$unei_name,$unei_genryo,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank,$unei_syoku)=split(/<>/);
			&time_get;
			if (($date_sec - $unei_yobi2) < (60*60*$unei_time)){&error("まだできない社員がいます。");}
			if($in{'par_suuti'} =~ /\D/){&error("値に誤りがあります。");}
			if ($kokugo < 0 || $suugaku < 0 || $rika < 0 || $syakai < 0 || $eigo < 0 || $ongaku < 0 || $bijutu < 0 || $looks < 0 || $tairyoku < 0 || $kenkou < 0 || $speed < 0 || $power < 0 || $wanryoku < 0 || $kyakuryoku < 0 || $love < 0 || $unique < 0 || $etti < 0){&error("パラメータが足りません。親はすべてのパラメータにおいてプラスである必要があります。");}
			if ($money < $youikuhi * @all_unei){&error("お金が足りません");}
		}
	}
	
	foreach (@all_unei){

		$youikuhi = 0;
		$unei_yobi3 = "";
		$message_in ="";

		($unei_num,$unei_name,$unei_genryo,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank,$unei_syoku)=split(/<>/);#koko2008/08/18
		chomp $unei_syoku;
#koko2008/08/18
#		if($genryou == 1){
#			$unei_kokugo = int($unei_kokugo *0.9);
#			$unei_suugaku = int($unei_suugaku *0.9);
#			$unei_rika = int($unei_rika *0.9);
#			$unei_syakai = int($unei_syakai *0.9);
#			$unei_eigo = int($unei_eigo *0.9);
#			$unei_ongaku = int($unei_ongaku *0.9);
#			$unei_bijutu = int($unei_bijutu *0.9);
#			$unei_looks = int($unei_looks *0.9);
#			$unei_tairyoku = int($unei_tairyoku *0.9);
#			$unei_kenkou = int($unei_kenkou *0.9);
#			$unei_speed = int($unei_speed *0.9);
#			$unei_power = int($unei_power *0.9);
#			$unei_wanryoku = int($unei_wanryoku *0.9);
#			$unei_kyakuryoku = int($unei_kyakuryoku *0.9);
#			$unei_love = int($unei_love *0.9);
#			$unei_unique = int($unei_unique *0.9);
#			$unei_etti = int($unei_etti *0.9);
#			$unei_syoku = int($unei_syoku *0.9);

#			$genryou = 0;
#		}
#end8/18
		if (!$unei_yobi5){$unei_yobi5 = $unei_yobi5s;}
		if (!$unei_yobi6){$unei_yobi6 = $unei_yobi6s;}

#パラメータアップの場合
		if (($in{'command'} eq "do_unei" && $in{'syain'} == $i) or $in{'command'} eq "do_unei2"){#改造しました
#unei_yobi1＝出産時間（秒）unei_yobi2＝最後に子育てした時間　unei_yobi3＝最後の子育てコメント　unei_yobi4＝トータル能力値　unei_yobi5＝身長　unei_yobi6＝体重　unei_yobi7＝最後の食事時間　unei_yobi8＝自立フラグ　unei_yobi9＝最後に子育てした人
		#	if ($in{'unei_num'} eq "$unei_num"){
		#		$sodate_taisyou_flg=1;
			&time_get;
			if (($date_sec - $unei_yobi2) < (60*60*$unei_time)){&error("まだできません。");}

			$konoagatta_suuti = int($in{'par_suuti'}/$unei_koritu);
			if($in{'par_suuti'} =~ /\D/){&error("値に誤りがあります。");}
	
			if ($in{'nouryoku'} eq "国語") { $unei_kokugo += $konoagatta_suuti; $kokugo -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "数学") { $unei_suugaku += $konoagatta_suuti; $suugaku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "理科") { $unei_rika += $konoagatta_suuti; $rika -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "社会") { $unei_syakai += $konoagatta_suuti; $syakai -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "英語") { $unei_eigo += $konoagatta_suuti; $eigo -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "音楽") { $unei_ongaku += $konoagatta_suuti; $ongaku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "美術") { $unei_bijutu += $konoagatta_suuti; $bijutu -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "体力") { $unei_tairyoku += $konoagatta_suuti; $tairyoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "健康") { $unei_kenkou += $konoagatta_suuti; $kenkou -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "スピード") { $unei_speed += $konoagatta_suuti; $speed -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "パワー") { $unei_power += $konoagatta_suuti; $power -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "腕力") { $unei_wanryoku += $konoagatta_suuti; $wanryoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "脚力") { $unei_kyakuryoku += $konoagatta_suuti; $kyakuryoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "ルックス") { $unei_looks += $konoagatta_suuti; $looks -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "LOVE") { $unei_love += $konoagatta_suuti; $love -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "面白さ") { $unei_unique += $konoagatta_suuti; $unique -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "エッチ") { $unei_etti += $konoagatta_suuti; $etti -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "食材購入"){ $unei_syoku += 0.1*$konoagatta_suuti; }

			if ($kokugo < 0 || $suugaku < 0 || $rika < 0 || $syakai < 0 || $eigo < 0 || $ongaku < 0 || $bijutu < 0 || $looks < 0 || $tairyoku < 0 || $kenkou < 0 || $speed < 0 || $power < 0 || $wanryoku < 0 || $kyakuryoku < 0 || $love < 0 || $unique < 0 || $etti < 0){&error("パラメータが足りません。親はすべてのパラメータにおいてプラスである必要があります。");}
#最後の子育て時間を更新
			$unei_yobi2 = $date_sec;
	
			$youikuhi = $konoagatta_suuti * $kyouikuhiyou;
			$unei_yobi3 = "社員教育で$in{'nouryoku'}パラメータを$konoagatta_suutiあげました（$date2）";
			$message_in ="社員教育で$in{'nouryoku'}パラメータが$konoagatta_suutiあがりました。運営費として$youikuhi円かかりました。";
				#koko
			if ($in{'siharaihouhou'} ne "現金"){
				$bank -= $youikuhi;
				&kityou_syori("クレジット支払い（運営費用）","$youikuhi","",$bank,"普");
			}else{
				if ($money < $date_hiyou){&error("お金が足りません");}
				$money -= $youikuhi;
			}
			if($in{'kouken'}){$unei_name = $in{'kouken'};} #koko2008/11/03


		}
#総合能力値計算
		$sogo_sisuu = ($unei_yobi5 + $unei_yobi6)/20;
		$unei_yobi4 = int (($unei_kokugo + $unei_suugaku + $unei_rika + $unei_syakai + $unei_eigo + $unei_ongaku + $unei_bijutu + $unei_looks + $unei_tairyoku + $unei_kenkou + $unei_speed + $unei_power + $unei_wanryoku + $unei_kyakuryoku + $unei_love + $unei_unique + $unei_etti)*$sogo_sisuu);

		&jyob_machi3;
		$siokuri_kingaku2 += $siokuri_kingaku1;

		$unei_job = $return_job;
		$unei_yobi8 = 1;
#koko2007/05/30
		if ($unei_kokugo >= $max_kokugo){$max_kokugo = $unei_kokugo;$maxkokugo = int($max_kokugo/10);}
		if ($unei_suugaku >= $max_suugaku){$max_suugaku = $unei_suugaku;$maxsuugaku = int($max_suugaku/10);}
		if ($unei_rika >= $max_rika){$max_rika = $unei_rika;$maxrika =int($max_rika/10);}
		if ($unei_syakai >= $max_syakai){$max_syakai = $unei_syakai;$maxsyakai =int($max_syakai/10);}
		if ($unei_eigo >= $max_eigo){$max_eigo = $unei_eigo;$maxeigo =int($max_eigo/10);}
		if ($unei_ongaku >= $max_ongaku){$max_ongaku = $unei_ongaku;$maxongaku =int($max_ongaku/10);}
		if ($unei_bijutu >= $max_bijutu){$max_bijutu = $unei_bijutu;$maxbijutu =int($max_bijutu/10);}
		if ($unei_looks >= $max_looks){$max_looks = $unei_looks;$maxlooks =int($max_looks/10);}
		if ($unei_tairyoku >= $max_tairyoku){$max_tairyoku = $unei_tairyoku;$maxtairyoku =int($max_tairyoku/10);}
		if ($unei_kenkou >= $max_kenkou){$max_kenkou = $unei_kenkou;$maxkenkou =int($max_kenkou/10);}
		if ($unei_speed >= $max_speed){$max_speed = $unei_speed;$maxspeed =int($max_speed/10);}
		if ($unei_power >= $max_power){$max_power = $unei_power;$maxpower =int($max_power/10);}
		if ($unei_wanryoku >= $max_wanryoku){$max_wanryoku = $unei_wanryoku;$maxwanryoku =int($max_wanryoku/10);}
		if ($unei_kyakuryoku >= $max_kyakuryoku){$max_kyakuryoku = $unei_kyakuryoku;$maxkyakuryoku =int($max_kyakuryoku/10);}
		if ($unei_love >= $max_love){$max_love = $unei_love;$maxlove =int($max_love/10);}
		if ($unei_unique >= $max_unique){$max_unique = $unei_unique;$maxunique =int($max_unique/10);}
		if ($unei_etti >= $max_etti){$max_etti = $unei_etti;$maxetti =int($max_etti/10);}
		if ($unei_syoku){$maxsyoku += $unei_syoku; }
		$taiku = $#all_unei+1;

		if (! -e "./member/$kaisya_id/itemyou.cgi"){ #koko2007/12/11
			$kakou = "<><><><>\n";
		}else{
			open(IN,"< ./member/$kaisya_id/itemyou.cgi") || &error("./member/$kaisya_id/itemyou.cgiに読み込めません"); #koko2007/12/11
			eval{ flock (IN, 1); };
			$genryou = <IN>;
			$kakou = <IN>;
			close(IN);
		}

		open(OUT,"> ./member/$kaisya_id/itemyou.cgi") || &error("./member/$kaisya_id/itemyou.cgiに書き込めません");
		eval{ flock (OUT, 2); };
		print OUT "$maxkokugo<>$maxsuugaku<>$maxrika<>$maxsyakai<>$maxeigo<>$maxongaku<>$maxbijutu<>$maxlooks<>$maxtairyoku<>$maxkenkou<>$maxspeed<>$maxpower<>$maxwanryoku<>$maxkyakuryoku<>$maxlove<>$maxunique<>$maxetti<>$maxsyoku<>$yo_karada_syou<>$yo_nou_syou<>$taiku<>\n";
		print OUT "$kakou";
		close(OUT);

#kokoend
		$new_uneiomo_temp0 = "$unei_num<>$unei_name<>$unei_oya1<>$unei_oya2<>$unei_job<>$unei_kokugo<>$unei_suugaku<>$unei_rika<>$unei_syakai<>$unei_eigo<>$unei_ongaku<>$unei_bijutu<>$unei_looks<>$unei_tairyoku<>$unei_kenkou<>$unei_speed<>$unei_power<>$unei_wanryoku<>$unei_kyakuryoku<>$unei_love<>$unei_unique<>$unei_etti<>$unei_yobi1<>$unei_yobi2<>$unei_yobi3<>$unei_yobi4<>$unei_yobi5<>$unei_yobi6<>$unei_yobi7<>$unei_yobi8<>$siokuri_kingaku1<>$ori_ie_rank<>$unei_syoku<>\n";
#	push (@new_all_uneiomo,$new_uneiomo_temp);
#	}	#foreach閉じ
#子供ログ更新
		push @new_uneiomo_temp,$new_uneiomo_temp0;
		if ($syinsyoukyo eq 'yes' && $syainjougen <= $#new_uneiomo_temp + 1){$#new_uneiomo_temp = $syainjougen - 1;}
		$i++;
	}
#パラメータアップの場合閉じ
	@all_unei = (@new_uneiomo_temp);
	open(KODO,">$unei_file") || &error("$unei_fileに書き込めません");
	eval{ flock (KODO, 2); };
	print KODO @new_uneiomo_temp;
	close(KODO);

#個人ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	

#所有物チェック koko
	if(!$k_id){&error("mono.cgi エラー kaishiya1")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
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

	&header(assen_style);

	$syain_limit = $syain_tantou * $yakuin_jougen;
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●自分の持っているパラメータを社員教育のために使ったりできます。<br>
●会社は与えたパラメータの$unei_koritu分の1しか得ることができません。<br>
●会社のパラメータ１に対して$kyouikuhiyou円の養育費がかかります。<br>
●社員教育できる間隔は$unei_time時間です。<br>
●社員総数は、$syainjougen人です。$syain_limit人が上限です。
</td>
<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:24px; color:#ffffff">社員教育</div>
</td></tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>$menba_list<br>
<div align=center>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="houmon">
<input type=hidden name=command value="kaisya_bbs">
<!-- <input type=hidden name=command value="kanrisya_up"> -->
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<!--<input type=hidden name=unei_num value="$unei_num">-->
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value=" 会社掲示板 ">
</form>
EOM

	if ($in{'name'} eq $kai_name_kanre){
		print <<"EOM";
<form method="POST" action="$this_script">
<input type=hidden name=mode value="seizou">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=unei_num value="$unei_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value=" 製造 ">$test
</form>
EOM
	}
	print <<"EOM";
</div>
</td></tr>
</table><br>
EOM
	if ($menba){
		print <<"EOM";
<iframe src="./syokugyo.htm" name="syokugyo" width="90%" height="250px" align=center></iframe>
<table width="90%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td><br></td></tr>
<tr><td>$kokugo</td><td>$suugaku</td><td>$rika</td><td>$syakai</td><td>$eigo</td><td>$ongaku</td><td>$bijutu</td><td>$looks</td><td><br></td></tr>
<tr><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td></tr>
<tr><td>$tairyoku</td><td>$kenkou</td><td>$speed</td><td>$power</td><td>$wanryoku</td><td>$kyakuryoku</td><td>$love</td><td>$unique</td><td>$etti</td></tr></table>
<table width="90%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>耐</td><td>個</td><td></tr>
<tr><td>$maxkokugo</td><td>$maxsuugaku</td><td>$maxrika</td><td>$maxsyakai</td><td>$maxeigo</td><td>$maxongaku</td><td>$maxbijutu</td><td>$maxlooks</td><td>$taiku<br></td><td>1</td></tr>
<tr><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td>食料</td></tr>
<tr><td>$maxtairyoku</td><td>$maxkenkou</td><td>$maxspeed</td><td>$maxpower</td><td>$maxwanryoku</td><td>$maxkyakuryoku</td><td>$maxlove</td><td>$maxunique</td><td>$maxetti</td><td>$maxsyoku</td></tr></table>
<br><br>

<div align="center">
<form method="POST" action="$this_script" style="margin-bottom: 0em">
<input type=hidden name=mode value="houmon">
<input type=hidden name=command value="do_unei2">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=unei_num value="$unei_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<select name=nouryoku>
<option value="国語">国語パラメータを</option>
<option value="数学">数学パラメータを</option>
<option value="理科">理科パラメータを</option>
<option value="社会">社会パラメータを</option>
<option value="英語">英語パラメータを</option>
<option value="音楽">音楽パラメータを</option>
<option value="美術">美術パラメータを</option>
<option value="体力">体力パラメータを</option>
<option value="健康">健康パラメータを</option>
<option value="スピード">スピードパラメータを</option>
<option value="パワー">パワーパラメータを</option>
<option value="腕力">腕力パラメータを</option>
<option value="脚力">脚力パラメータを</option>
<option value="ルックス">ルックスパラメータを</option>
<option value="LOVE">LOVEパラメータを</option>
<option value="面白さ">面白さパラメータを</option>
<option value="エッチ">エッチパラメータを</option>
<option value="食材購入">食材0.1キロカロリー</option>
</select>
<select name=par_suuti>
<option value="10" selected>10</option>
<option value="20">20</option>
<option value="30">30</option>
<option value="50">50</option>
<option value="80">80</option>
<option value="100">100</option>
<option value="200">200</option>
<option value="300">300</option>
<option value="500">500</option>
<option value="800">800</option>
<option value="1000">1000</option>
</select>
<font color="#ff0000"><b>÷$unei_koritu</b></font>　支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select>
<input type=submit value=" 全体をあげる ">
</form>
</div>
EOM

		$i=0;
		foreach (@all_unei){
			($unei_num,$unei_name,$unei_genryo,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank,$unei_syoku)=split(/<>/);#koko2008/08/18
			chomp $unei_syoku;

#持ち物フォーム作成
			$ii = $i +1;
			if($syainjougen -1 >= $i){
				print <<"EOM";
<table width="90%" border="0" cellspacing="0" align=center class=yosumi>
<tr bgcolor=#ffffaa><td>
<span class="honbun2">最後の教育：$unei_yobi3 by $unei_name</span></td></tr><!-- koko2008/11/03 -->
<tr bgcolor=#dddddd><td>
<form method="POST" action="$this_script" style="margin-bottom: 0em">
<input type=hidden name=mode value="houmon">
<input type=hidden name=command value="do_unei">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=unei_num value="$unei_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=kouken value="$name"><!-- koko2008/11/03 -->
<input type=hidden name=syain value="$i">
<select name=nouryoku>
<option value="国語">国語パラメータを</option>
<option value="数学">数学パラメータを</option>
<option value="理科">理科パラメータを</option>
<option value="社会">社会パラメータを</option>
<option value="英語">英語パラメータを</option>
<option value="音楽">音楽パラメータを</option>
<option value="美術">美術パラメータを</option>
<option value="体力">体力パラメータを</option>
<option value="健康">健康パラメータを</option>
<option value="スピード">スピードパラメータを</option>
<option value="パワー">パワーパラメータを</option>
<option value="腕力">腕力パラメータを</option>
<option value="脚力">脚力パラメータを</option>
<option value="ルックス">ルックスパラメータを</option>
<option value="LOVE">LOVEパラメータを</option>
<option value="面白さ">面白さパラメータを</option>
<option value="エッチ">エッチパラメータを</option>
<option value="食材購入">食材0.1キロカロリー</option>
</select>
 <select name=par_suuti>
<option value="10" selected>10</option>
<option value="20">20</option>
<option value="30">30</option>
<option value="50">50</option>
<option value="80">80</option>
<option value="100">100</option>
<option value="200">200</option>
<option value="300">300</option>
<option value="500">500</option>
<option value="800">800</option>
<option value="1000">1000</option>
</select>
<font color="#ff0000"><b>÷$unei_koritu</b></font>　支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select>
<input type=submit value=" あげる "> $ii
</form>
</td></tr></table>
EOM
				$i++;
				print <<"EOM"; # $return_job → $unei_job 2007/05/26
	<table width="90%" border="0" cellspacing="0" align=center class=yosumi>
	<tr><td><span class="honbun2">総合能\力値：</span>$unei_yobi4 $unei_job $siokuri_kingaku1円</td>
	<tr><td>
<table width="100%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国語</td><td>数学</td><td>理科</td><td>社会</td><td>英語</td><td>音楽</td><td>美術</td><td>ルックス</td><td><br></td></tr>
<tr><td>$unei_kokugo</td><td>$unei_suugaku</td><td>$unei_rika</td><td>$unei_syakai</td><td>$unei_eigo</td><td>$unei_ongaku</td><td>$unei_bijutu</td><td>$unei_looks</td><td><br></td></tr>
<tr><td>体力</td><td>健康</td><td>スピード</td><td>パワー</td><td>腕力</td><td>脚力</td><td>LOVE</td><td>面白さ</td><td>エッチ</td></tr>
<tr><td>$unei_tairyoku</td><td>$unei_kenkou</td><td>$unei_speed</td><td>$unei_power</td><td>$unei_wanryoku</td><td>$unei_kyakuryoku</td><td>$unei_love</td><td>$unei_unique</td><td>$unei_etti</td></tr></table>
	<td></tr></table>
EOM
			}
		}
		if ($in{'name'} eq $kai_name_kanre){
			if ($syainjougen > $#all_unei + 1){
				print <<"EOM";
<br><div align=center>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="houmon">
<input type=hidden name=command value="syain_up">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=unei_num value="$unei_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value=" 社員を増やす ">
</form></div>
EOM
			}
		}
	}else{

		foreach (@all_unei){
			($unei_num,$unei_name,$unei_genryo,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank,$unei_syoku)=split(/<>/);#koko2008/08/18
			chomp $unei_syoku;

			print <<"EOM";
<table width="90%" border="0" cellspacing="0" align=center class=yosumi>
<tr><td><span class="honbun2">総合能\力値：</span>$unei_yobi4 $return_job $siokuri_kingaku1円</td>
<tr><td>
<table width="100%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国語</td><td>数学</td><td>理科</td><td>社会</td><td>英語</td><td>音楽</td><td>美術</td><td>ルックス</td><td><br></td></tr>
<tr><td>$unei_kokugo</td><td>$unei_suugaku</td><td>$unei_rika</td><td>$unei_syakai</td><td>$unei_eigo</td><td>$unei_ongaku</td><td>$unei_bijutu</td><td>$unei_looks</td><td><br></td></tr>
<tr><td>体力</td><td>健康</td><td>スピード</td><td>パワー</td><td>腕力</td><td>脚力</td><td>LOVE</td><td>面白さ</td><td>エッチ</td></tr>
<tr><td>$unei_tairyoku</td><td>$unei_kenkou</td><td>$unei_speed</td><td>$unei_power</td><td>$unei_wanryoku</td><td>$unei_kyakuryoku</td><td>$unei_love</td><td>$unei_unique</td><td>$unei_etti</td></tr></table>
<td></tr></table>
EOM
		}
	}
	print "<div align=center><br>総合 $siokuri_kingaku2円<br></div>\n";

	&hooter("login_view","街へ戻る");
	exit;
}

#子供自立サブルーチン
sub jyob_machi3 {
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	my $top_koumoku = <SP>;
	my @job_hairetu = <SP>;
	close(SP);

	foreach  (@job_hairetu) {
		&job_sprit($_);
		$job_kihonkyuu{"$job_name"} = $job_kyuuyo;
	}

	@ko_keys = map {(split /<>/)[18]} @job_hairetu;
	@job_hairetu_sort = @job_hairetu[sort {$ko_keys[$b] <=> $ko_keys[$a]} 0 .. $#ko_keys];

#条件を満たしている職業を検索
	foreach (@job_hairetu_sort){
		&job_sprit($_);
		if($unei_kokugo < $job_kokugo){next;}
		if($unei_suugaku < $job_suugaku){next;}
		if($unei_rika < $job_rika){next;}
		if($unei_syakai < $job_syakai){next;}
		if($unei_eigo < $job_eigo){next;}
		if($unei_ongaku < $job_ongaku){next;}
		if($unei_bijutu < $job_bijutu){next;}
	#	if($BMI < $job_BMI_min){next;}
	#	if ($job_BMI_max) { if($BMI > $job_BMI_max){next;}}
		if($unei_looks < $job_looks){next;}
		if($unei_tairyoku < $job_tairyoku){next;}
		if($unei_kenkou < $job_kenkou){next;}
		if($unei_speed < $job_speed){next;}
		if($unei_power < $job_power){next;}
		if($unei_wanryoku < $job_wanryoku){next;}
		if($unei_kyakuryoku < $job_kyakuryoku){next;}
		if($unei_love < $job_love){next;}
		if($unei_unique < $job_unique){next;}
		if($unei_etti < $job_etti){next;}
	#	if($unei_yobi5 < $job_sintyou){next;} #koko2007/06/30
		last;
	}	#foreach閉じ
		if ($job_name eq ""){$job_name = "浮浪者";}
		$return_job = $job_name;


		$siokuri_kingaku1 = ($job_kihonkyuu{"$unei_job"} * 10) + ($unei_yobi4 * 10);
		$siokuri_kingaku1 = int ($siokuri_kingaku1 / 4);

}
######会社ＢＢＳ
sub kaisya_bbs {
#	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."$bangou";

	($kaisya_id,$bangou) = split(/_/,$in{'ori_ie_id'});
#   if ($_[0] eq 'ok'){
	open (KAISYA,"< ./member/$kaisya_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_bbs.cgi");
	eval{ flock (KAISYA, 1); };
	$kanri_bbs = <KAISYA>;
	@kiji_bbs = <KAISYA>;
	close(KAISYA);

	($opn_no,$men_no,$kai0_id,$kai_name_kanre,$kaitime,$kakikomijikan,$yomidashijikan) = split(/<>/,$kanri_bbs); #koko2007/05/29
	chomp $kakikomijikan;
	chomp $yomidashijikan;

	open (KAISYA,"< ./member/$kaisya_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_kanri.cgi");
	eval{ flock (KAISYA, 1); };
	$ouna = <KAISYA>;
	@yakuin_list = <KAISYA>;
	close(KAISYA);

	($tmp_id,$tmp_name,$tmp_time) = split(/<>/,$ouna);
	$menba = "";
	$sankakyohi = "";

	foreach (@yakuin_list){
		($kai_id,$kai_name,$kai_time) = split(/<>/);
		if ($in{'name'} eq $kai_name){
			$menba = $kai_name;
		}
		$menba_list .= "$kai_name,";
		if ($in{'name'} eq $tmp_name){
			$sankakyohi .= "<input type=radio name=taikai value=\"$kai_name\">$kai_name \n"
		}
	}
	if ($tmp_name eq $in{'name'}){
		$menba = $tmp_name;
	}

	@kiji_bbs_opn = ();
	@kiji_bbs_men = ();
	foreach $temp (@kiji_bbs){
		($kigisybetu,$kijibangou,$kai0_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/,$temp);
		if ($kigisybetu eq 'kaisya_opn'){
			push @kiji_bbs_opn,$temp;
		}elsif($kigisybetu eq 'kaisya_men'){
			push @kiji_bbs_men,$temp;
		}
	}
#  }
	if($yakuin_jougen >= $#yakuin_list + 1){
		$niukaikibu = "●入会希望 <input type=checkbox name=niyukai value=\"in\">";
	}
	if($in{'name'} eq $kai_name_kanre){$taikaishitei = "退会指定 $sankakyohi<br>\n";}

	&header(assen_style);

	print <<"EOM";
<table width="100%" border="0" cellspacing="10" cellpadding="0" align=center>
<tr><td width=50% valign=top>
<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
<tr><td>
<div class=tyuu>■メッセージ来訪者</div>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="kaisya_bbs_do">
<input type=hidden name=bunrui value="kaisya_opn">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
●メッセージ<br>
<textarea cols=58 rows=8 name=m_com wrap="soft"></textarea><br>
<!--	●入会・解雇<br> -->
$niukaikibu<br>
$taikaishitei
<div align=center><input type="submit" value=" O K "></div>
</form></td></tr></table>
<br>
<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
<tr><td>
<div class=tyuu>来訪者掲示板</div><br>
EOM
	foreach (@kiji_bbs_opn){
		($kigisybetu,$kijibangou,$kai0_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/);

		if ($tokusyu eq 'in' && $in{'name'} eq $kai_name_kanre){
			$disp_tokusyu = "<form method=\"POST\" action=\"$this_script\"><input type=hidden name=mode value=\"kaisya_bbs_do\"><input type=hidden name=bunrui value=\"kaisya_opn\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=hidden name=tokusyu value=\"$tokusyu\"><input type=hidden name=namae value=\"$kaitaname\"><input type=hidden name=kyoka value=\"kyoka\"><input type=\"submit\" value=\"入会\"></form><br>\n";
		}elsif($tokusyu eq 'm_ryoukai'){
			$disp_tokusyu = "入会受領<br>\n";
		}elsif($tokusyu eq 'in'){
			$disp_tokusyu = "入会申\請中<br>\n";
		}elsif($tokusyu eq  'taikai'){
			$disp_tokusyu = "退会指定<br>\n";
		}else{
			$disp_tokusyu ="";
		}
		print "$kijibangou : $kaitaname<br>$disp_tokusyu : $kcoment<br><br>\n";
	}

	print <<"EOM";
</td></tr></table>
EOM

	if ($menba){
		print <<"EOM";
</td><td width=50% valign=top>
<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
<tr><td>
<div class=tyuu>■メッセージメンバー</div>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="kaisya_bbs_do">
<input type=hidden name=bunrui value="kaisya_men">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
●メッセージ<br>
<textarea cols=58 rows=8 name=m_com wrap="soft"></textarea><br>
●退会希望<input type=checkbox name=niyukai value="out"><br>
<div align=center><input type="submit" value=" O K "></div>
</form></td></tr></table>
<br>
<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
<tr><td>
<div class=tyuu>メンバー掲示板</div><br>
EOM
	foreach (@kiji_bbs_men){
		($kigisybetu,$kijibangou,$kai0_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/);

		if ($tokusyu eq 'out' && $in{'name'} eq $kai_name_kanre){
			$disp_tokusyu = "<form method=\"POST\" action=\"$this_script\"><input type=hidden name=mode value=\"kaisya_bbs_do\"><input type=hidden name=bunrui value=\"kaisya_men\"><input type=hidden name=ori_ie_id value=\"$in{'ori_ie_id'}\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=hidden name=tokusyu value=\"$tokusyu\"><input type=hidden name=namae value=\"$kaitaname\"><input type=hidden name=kyoka value=\"kyoka\"><input type=\"submit\" value=\"退会\"></form><br>\n";
		}elsif($tokusyu eq 'm_ryoukai'){
			$disp_tokusyu = "退会受領<br>\n";
		}elsif($tokusyu eq 'out'){
			$disp_tokusyu = "退会申\請中<br>\n";
		}else{
			$disp_tokusyu ="";
		}
		print "$kijibangou : $kaitaname<br>$disp_tokusyu : $kcoment<br><br>\n";
	}
	print <<"EOM";
</td></tr></table>
EOM
	}

	print "</table>\n";

#-------　フォーム要素名　---------
#print "<table border='1'>";
#print "<tr><th>フォーム要素名</th><th>データ</th></tr>";

#foreach $key (keys %in) {
#	print "<tr><th>$key</th><td>$in{$key}</td></tr>\n";
#}
#print "</table><br>";
	if ($tmp_name eq $in{'name'}){
#koko2007/05/29
		$yomidashijikan = time;
		$kanri_bbs = "$opn_no<>$men_no<>$kai0_id<>$kai_name_kanre<>$date2<>$kakikomijikan<>$yomidashijikan<>\n";
		open (OUT,"> ./member/$kaisya_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_bbs.cgi");
		eval{ flock (OUT, 2); };
		print OUT $kanri_bbs;
		print OUT @kiji_bbs;
		close(OUT);
#kokoend
		print <<EOM;
<div align=center>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="kaisya_bbs_do">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=radio name=bunrui value="kaisya_opn">オープン掲示板
<input type=radio name=bunrui value="kaisya_men">メンバー掲示板
<input type=text name=del_no>番号
<input type="submit" value="削除"></form></div><br>
EOM
	}
	&hooter("login_view","家を出る");
	exit;
}

#### 会社書き込み処理
sub kaisya_bbs_do {
	if (!$in{'m_com'} && !($in{'tokusyu'} && $in{'kyoka'}) && !$in{'del_no'}){&kaisya_bbs;}
	if (length($in{'m_com'}) > 1000) {&error("挨拶は500字以内です");}
	($kaisya_id,$bangou) = split(/_/,$in{'ori_ie_id'});
	open (KAISYA,"< ./member/$kaisya_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_bbs.cgi");
	eval{ flock (KAISYA, 1); };
	$kanri_bbs = <KAISYA>;
	@kiji_bbs = <KAISYA>;
	close(KAISYA);

	($opn_no,$men_no,$kai0_id,$kai_name_kanre,$kaitime,$kakikomijikan,$yomidashijikan) = split(/<>/,$kanri_bbs); #koko2007/05/29
	chomp $kakikomijikan;
	chomp $yomidashijikan;

	@kiji_bbs_opn =();
	@kiji_bbs_men =();
	foreach $temp(@kiji_bbs){
		($kigisybetu,$kijibangou,$kai0_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/,$temp);
		if ($kigisybetu eq 'kaisya_opn'){
			if ($in{'del_no'} eq $kijibangou && $in{'bunrui'} eq 'kaisya_opn'){
				next;
			}else{
				push @kiji_bbs_opn,$temp;
			}
		}elsif ($kigisybetu eq 'kaisya_men'){
			if ($in{'del_no'} eq $kijibangou && $in{'bunrui'} eq 'kaisya_men'){
				next;
			}else{
				push @kiji_bbs_men,$temp;
			}
		}
	}


	open (KAISYA,"< ./member/$kaisya_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_kanri.cgi");
	eval{ flock (KAISYA, 1); };
	$ouna = <KAISYA>;
	@yakuin_list = <KAISYA>;
	close(KAISYA);

	($kai_id_o,$kai_name_o,$kai_time_o) = split(/<>/,$ouna);

	&time_get; #$date2 受け取り

	$henkou = 0;
	@kiji_bbs_men0 = ();

	if ($in{'taikai'}){
		@yakuin_list0 =();
		foreach (@yakuin_list){
			($kai_id,$kai_name,$kai_time) = split(/<>/);
			if ($in{'taikai'} eq $kai_name){
				$opn_no++;
				$in{'m_com'} = "退会者：$in{'taikai'}<br>: $in{'m_com'}"; #koko2007/06/10
				unshift @kiji_bbs_opn,"kaisya_opn<>$opn_no<>$in{'id'}<>$in{'name'}<>$in{'m_com'}<>taikai<>$date2<>\n";
				if ($#kiji_bbs_opn + 1 >= 30){$#kiji_bbs_opn = 29;}
				next;
			}
			push @yakuin_list0,"$kai_id<>$kai_name<>$kai_time<>\n";
		}
		@yakuin_list = (@yakuin_list0);
	}

	$henkou = 0;
	@yakuin_list0 = ();
	@kiji_bbs_men0 = ();

	if ($in{'name'} eq $kai_name_o){
		$in{'niyukai'} = "";
	}

	if ($in{'tokusyu'} eq 'in' && $in{'kyoka'}){  # 入会処理
		foreach (@yakuin_list){
			($kai_id,$kai_name,$kai_time) = split(/<>/);
			if ($kai_name eq $in{'namae'}){
				$nijyutoroku = 1;
			}
		}

		if (!$nijyutoroku || !($in{'name'} eq $kai_name_kanre)){
#koko2007/06/10
			&id_check($in{'namae'});
			$kai_id = $return_id;
#kokoend
			push @yakuin_list,"$kai_id<>$in{'namae'}<>$date2<>\n";
			if ($#yakuin_list >= 30){$#yakuin_list = 29;}
		}

		@kiji_bbs_0 =();
		foreach (@kiji_bbs_opn){
			($kigisybetu,$kijibangou,$kai_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/);
			if ($kaitaname eq $in{'namae'} && $tokusyu eq 'in'){
				$tokusyu = 'm_ryoukai';
				$henkou = 1;
			}
			push @kiji_bbs_0,"$kigisybetu<>$kijibangou<>$kai0_id<>$kaitaname<>$kcoment<>$tokusyu<>$jikan<>\n";
		}
		if ($henkou){
			@kiji_bbs_opn = (@kiji_bbs_0);
		}
	}
	$henkou = 0;
	@yakuin_list0 =();
	@kiji_bbs_opn0 = ();
	if ($in{'tokusyu'} eq 'out' && $in{'kyoka'}){ # 退会処理
		@kiji_bbs_men0 =();
		foreach (@kiji_bbs_men){
			($kigisybetu,$kijibangou,$kai0_id,$kaitaname,$kcoment,$tokusyu,$jikan) = split(/<>/,);
			if ($kaitaname eq $in{'namae'} && $in{'tokusyu'} eq 'out'){
				$tokusyu = 'm_ryoukai';
			}
			push @kiji_bbs_men0,"$kigisybetu<>$kijibangou<>$kai0_id<>$kaitaname<>$kcoment<>$tokusyu<>$jikan<>\n";
			$henkou = 1;
		}
		@kiji_bbs_men = (@kiji_bbs_men0);
		@yakuin_list0 =();
		foreach (@yakuin_list){
			($kai_id,$kai_name,$kai_time) = split(/<>/);
			if ($kai_name eq $in{'namae'}){
				next;
			}
			push @yakuin_list0,"$kai_id<>$kai_name<>$kai_time<>\n";
		}
		if($henkou){
			@kiji_bbs_men = (@kiji_bbs_men0);
			@yakuin_list = (@yakuin_list0);
		}
	}
# #コメント書き込み
	if($in{'m_com'} && !$in{'taikai'}){
		if ($in{'bunrui'} eq 'kaisya_opn'){
			if ($nijyutoroku){
				$in{'niyukai'} = 'm_ryoukai';
			}
			$opn_no++;
			unshift @kiji_bbs_opn,"$in{'bunrui'}<>$opn_no<>$in{'id'}<>$in{'name'}<>$in{'m_com'}<>$in{'niyukai'}<>$date2<>\n";
			if ($#kiji_bbs_opn + 1 >= 30){$#kiji_bbs_opn = 29;}
		}elsif($in{'bunrui'} eq 'kaisya_men'){
			$men_no++;
			unshift @kiji_bbs_men,"$in{'bunrui'}<>$men_no<>$in{'id'}<>$in{'name'}<>$in{'m_com'}<>$in{'niyukai'}<>$date2<>\n";
			if ($#kiji_bbs_men+1 >= 30){$#kiji_bbs_men = 29;}
		}

		if ($in{'name'} ne $kai_name_kanre){$kakikomijikan = time;} #koko2007/05/29

	}

	@kiji_bbs =(@kiji_bbs_opn,@kiji_bbs_men);
	$kanri_bbs = "$opn_no<>$men_no<>$kai0_id<>$kai_name_kanre<>$date2<>$kakikomijikan<>$yomidashijikan<>\n";#koko2007/05/29


	open (KAISYA,"> ./member/$kaisya_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_kanri.cgi");
	eval{ flock (KAISYA, 2); };
	print KAISYA $ouna;
	print KAISYA @yakuin_list;
	close(KAISYA);

	open (OUT,"> ./member/$kaisya_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$kaisya_id/kaishiya_bbs.cgi");
	eval{ flock (OUT, 2); };
	print OUT $kanri_bbs;
	print OUT @kiji_bbs;
	close(OUT);

	&kaisya_bbs;
	exit;

}
#### 製造 ####
sub seizou {
	open(IN,"< ./member/$k_id/itemyou.cgi") || &error("./member/$k_id/itemyou.cgiに読み込めません");
	eval{ flock (IN, 1); };
	$genryou = <IN>;
	$kakou = <IN>;
	close(IN);

	($kakou_day,$hinmei,$no,$day_tim) = split(/<>/,$kakou); #koko2007/12/10

	($maxkokugo,$maxsuugaku,$maxrika,$maxsyakai,$maxeigo,$maxongaku,$maxbijutu,$maxlooks,$maxtairyoku,$maxkenkou,$maxspeed,$maxpower,$maxwanryoku,$maxkyakuryoku,$maxlove,$maxunique,$maxetti,$maxsyoku,$yo_karada_syou,$yo_nou_syou,$taiku) = split(/<>/,$genryou);

	open(IN,"< ./member/$k_id/omise_ini.cgi") || &error("./member/$k_id/omise_ini.cgiに読み込めません");
	eval{ flock (IN, 1); };
	$omise_ini = <IN>;
	close(IN);

	(@mise_kubun) = split(/<>/,$omise_ini); #$mise_kubun[3];


	if (!$in{'kai_hinmoku'}){
		if (!$hinmei){
			$i_hinmei = "$nameの商品";
		}else{
			$i_hinmei = "$hinmei"; #koko2007/12/16
		}
	}else{
		$i_hinmei = "$in{'kai_hinmoku'}"; #koko2007/12/16
	}

	$i_hinmei =~ s/ //g;

	 #koko2007/09/24
	if (!$in{'kai_comment'}){
		if (!$i_comment){
			$i_comment = "【備考】";
		}else{
			$i_comment = "$i_hinmei";
		}
	}else{
		$i_comment = $in{'kai_comment'};
	}
#koko2007/12/17
	if ($in{'kai_kokugo'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_suugaku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_rika'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_syakai'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_eigo'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_ongaku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_bijutu'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_looks'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_tairyoku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_kenkou'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_speed'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_power'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_wanryoku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_kyakuryoku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_love'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_unique'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_etti'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_cal'} =~ /[^0-9\.]/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_kankaku'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_sintai_syouhi'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_zunou_syouhi'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_zaiko'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_taikyuu'} =~ /\D/){&error("数値以外に設定しないでください。");}
	if ($in{'kai_nedan'} =~ /\D/){&error("数値以外に設定しないでください。");}
#kokoend
	if ($in{'kai_kokugo'} < 0){$in{'kai_kokugo'} = 0;}elsif ($in{'kai_kokugo'} > $maxkokugo){$in{'kai_kokugo'} = $maxkokugo;}
	if ($in{'kai_suugaku'} < 0){$in{'kai_suugaku'} = 0;}elsif ($in{'kai_suugaku'} > $maxsuugaku){$in{'kai_suugaku'} = $maxkosuugaku;}
	if ($in{'kai_rika'} < 0){$in{'kai_rika'} = 0;}elsif ($in{'kai_rika'} > $maxrika){$in{'kai_rika'} = $maxrika;}
	if ($in{'kai_syakai'} < 0){$in{'kai_syakai'} = 0;}elsif ($in{'kai_syakai'} > $maxsyakai){$in{'kai_syakai'} = $maxsyakai;}
	if ($in{'kai_eigo'} < 0){$in{'kai_eigo'} = 0;}elsif ($in{'kai_eigo'} > $maxeigo){$in{'kai_eigo'} = $maxeigo;}
	if ($in{'kai_ongaku'} < 0){$in{'kai_ongaku'} = 0;}elsif ($in{'kai_ongaku'} > $maxongaku){$in{'kai_ongaku'} = $maxongaku;}
	if ($in{'kai_bijutu'} < 0){$in{'kai_bijutu'} = 0;}elsif ($in{'kai_bijutu'} > $maxbijutu){$in{'kai_bijutu'} = $maxbijutu;}
	if ($in{'kai_looks'} < 0){$in{'kai_looks'} = 0;}elsif ($in{'kai_looks'} > $maxlooks){$in{'kai_looks'} = $maxlooks;}
	if ($in{'kai_tairyoku'} < 0){$in{'kai_tairyoku'} = 0;}elsif ($in{'kai_tairyoku'} > $maxtairyoku){$in{'kai_tairyoku'} = $maxtairyoku;}
	if ($in{'kai_kenkou'} < 0){$in{'kai_kenkou'} = 0;}elsif ($in{'kai_kenkou'} > $maxkenkou){$in{'kai_kenkou'} = $maxkenkou;}
	if ($in{'kai_speed'} < 0){$in{'kai_speed'} = 0;}elsif ($in{'kai_speed'} > $maxspeed){$in{'kai_speed'} = $maxspeed;}
	if ($in{'kai_power'} < 0){$in{'kai_power'} = 0;}elsif ($in{'kai_power'} > $maxpower){$in{'kai_power'} = $maxpower;}
	if ($in{'kai_wanryoku'} < 0){$in{'kai_wanryoku'} = 0;}elsif ($in{'kai_wanryoku'} > $maxwanryoku){$in{'kai_wanryoku'} = $maxwanryoku;}
	if ($in{'kai_kyakuryoku'} < 0){$in{'kai_kyakuryoku'} = 0;}elsif ($in{'kai_kyakuryoku'} > $maxkyakuryoku){$in{'kai_kyakuryoku'} = $maxkyakuryoku;}
	if ($in{'kai_love'} < 0){$in{'kai_love'} = 0;}elsif ($in{'kai_love'} > $maxlove){$in{'kai_love'} = $maxlove;}
	if ($in{'kai_unique'} < 0){$in{'kai_unique'} = 0;}elsif ($in{'kai_unique'} > $maxunique){$in{'kai_unique'} = $maxunique;}
	if ($in{'kai_etti'} < 0){$in{'kai_etti'} = 0;}elsif ($in{'kai_etti'} > $maxetti){$in{'kai_etti'} = $maxetti;}
	if ($in{'kai_cal'} < 0){$in{'kai_cal'} = 0;}elsif ($in{'kai_cal'} > $maxsyoku){$in{'kai_cal'} = $maxsyoku;}
	if ($in{'kai_kankaku'} < 0){$in{'kai_kankaku'} = 0;}

	if ($maxkokugo){$b_kokugo=1;}
	if ($maxsuugaku){$b_suugaku=1;}
	if ($maxrika){$b_rika=1;}
	if ($maxsyakai){$b_syakai=1;}
	if ($maxeigo){$b_eigo=1;}
	if ($maxongaku){$b_ongaku=1;}
	if ($maxbijutu){$b_bijutu=1;}
	if ($maxlooks){$b_looks=1;}
	if ($maxtairyoku){$b_tairyoku=1;}
	if ($maxkenkou){$b_kenkou=1;}
	if ($maxspeed){$b_speed=1;}
	if ($maxpower){$b_power=1;}
	if ($maxwanryoku){$b_wanryoku=1;}
	if ($maxkyakuryoku){$b_kyakuryoku=1;}
	if ($maxlove){$b_love=1;}
	if ($maxunique){$b_unique=1;}
	if ($maxetti){$b_etti=1;}
	if ($maxsyoku){$b_cal=1;}

	if ($in{'kai_kokugo'}){
		if($in{'kai_kokugo'} <= 500){
			$i_kokugo=$in{'kai_kokugo'};
			$b_kokugo=int($maxkokugo/$in{'kai_kokugo'});
		}else{
			$i_kokugo=500;
			$b_kokugo=int($maxkokugo/500);
		}
	}else{
		if($in{'kai_kokugo'} eq "0"){
			$i_kokugo=0;
			$b_kokugo=$maxkokugo;
		}else{
			$i_kokugo=$maxkokugo;
		}
	}
	if ($in{'kai_suugaku'}){
		if($in{'kai_suugaku'} <= 500){
			$i_suugaku=$in{'kai_suugaku'};
			$b_suugaku=int($maxsuugaku/$in{'kai_suugaku'});
		}else{
			$i_suugaku=500;
			$b_suugaku=int($maxsuugaku/500);
		}
	}else{
		if($in{'kai_suugaku'} eq "0"){
			$i_suugaku=0;
			$b_suugaku=$maxsuugaku;
		}else{
			$i_suugaku=$maxsuugaku;
		}
	}
	if ($in{'kai_rika'}){
		if($in{'kai_rika'} <= 500){
			$i_rika=$in{'kai_rika'};
			$b_rika=int($maxrika/$in{'kai_rika'});
		}else{
			$i_rika=500;
			$b_rika=int($maxrika/500);
		}
	}else{
		if($in{'kai_rika'} eq "0"){
			$i_rika=0;
			$b_rika=$maxrika;
		}else{
			$i_rika=$maxrika;
		}
	}
	if ($in{'kai_syakai'}){
		if($in{'kai_syakai'} <= 500){
			$i_syakai=$in{'kai_syakai'};
			$b_syakai=int($maxsyakai/$in{'kai_syakai'});
		}else{
			$i_syakai=500;
			$b_syakai=int($maxsyakai/500);
		}
	}else{
		if($in{'kai_syakai'} eq "0"){
			$i_syakai=0;
			$b_syakai=$maxsyakai;
		}else{
			$i_syakai=$maxsyakai;
		}
	}
	if ($in{'kai_eigo'}){
		if($in{'kai_eigo'} <= 500){
			$i_eigo=$in{'kai_eigo'};
			$b_eigo=int($maxeigo/$in{'kai_eigo'});
		}else{
			$i_eigo=500;
			$b_eigo=int($maxeigo/500);
		}
	}else{
		if($in{'kai_eigo'} eq "0"){
			$i_eigo=0;
			$b_eigo=$maxeigo;
		}else{
			$i_eigo=$maxeigo;
		}
	}
	if ($in{'kai_ongaku'}){
		if($in{'kai_ongaku'} <= 500){
			$i_ongaku=$in{'kai_ongaku'};
			$b_ongaku=int($maxongaku/$in{'kai_ongaku'});
		}else{
			$i_ongaku=500;
			$b_ongaku=int($maxongaku/500);
		}
	}else{
		if($in{'kai_ongaku'} eq "0"){
			$i_ongaku=0;
			$b_ongaku=$maxongaku;
		}else{
			$i_ongaku=$maxongaku;
		}
	}
	if ($in{'kai_bijutu'}){
		if($in{'kai_bijutu'} <= 500){
			$i_bijutu=$in{'kai_bijutu'};
			$b_bijutu=int($maxbijutu/$in{'kai_bijutu'});
		}else{
			$i_bijutu=500;
			$b_bijutu=int($maxbijutu/500);
		}
	}else{
		if($in{'kai_bijutu'} eq "0"){
			$i_bijutu=0;
			$b_bijutu=$maxbijutu;
		}else{
			$i_bijutu=$maxbijutu;
		}
	}
	if ($in{'kai_looks'}){
		if($in{'kai_looks'} <= 500){
			$i_looks=$in{'kai_looks'};
			$b_looks=int($maxlooks/$in{'kai_looks'});
		}else{
			$i_looks=500;
			$b_looks=int($maxlooks/500);
		}
	}else{
		if($in{'kai_looks'} eq "0"){
			$i_looks=0;
			$b_looks=$maxlooks;
		}else{
			$i_looks=$maxlooks;
		}
	}
	if ($in{'kai_tairyoku'}){
		if($in{'kai_tairyoku'} <= 500){
			$i_tairyoku=$in{'kai_tairyoku'};
			$b_tairyoku=int($maxtairyoku/$in{'kai_tairyoku'});
		}else{
			$i_tairyoku=500;
			$b_tairyoku=int($maxtairyoku/500);
		}
	}else{
		if($in{'kai_tairyoku'} eq "0"){
			$i_tairyoku=0;
			$b_tairyoku=$maxtairyoku;
		}else{
			$i_tairyoku=$maxtairyoku;
		}
	}
	if ($in{'kai_kenkou'}){
		if($in{'kai_kenkou'} <= 500){
			$i_kenkou=$in{'kai_kenkou'};
			$b_kenkou=int($maxkenkou/$in{'kai_kenkou'});
		}else{
			$i_kenkou=500;
			$b_kenkou=int($maxkenkou/500);
		}
	}else{
		if($in{'kai_kenkou'} eq "0"){
			$i_kenkou=0;
			$b_kenkou=$maxkenkou;
		}else{
			$i_kenkou=$maxkenkou;
		}
	}
	if ($in{'kai_speed'}){
		if($in{'kai_speed'} <= 500){
			$i_speed=$in{'kai_speed'};
			$b_speed=int($maxspeed/$in{'kai_speed'});
		}else{
			$i_speed=500;
			$b_speed=int($maxspeed/500);
		}
	}else{
		if($in{'kai_speed'} eq "0"){
			$i_speed=0;
			$b_speed=$maxspeed;
		}else{
			$i_speed=$maxspeed;
		}
	}
	if ($in{'kai_power'}){
		if($in{'kai_power'} <= 500){
			$i_power=$in{'kai_power'};
			$b_power=int($maxpower/$in{'kai_power'});
		}else{
			$i_power=500;
			$b_power=int($maxpower/500);
		}
	}else{
		if($in{'kai_power'} eq "0"){
			$i_power=0;
			$b_power=$maxpower;
		}else{
			$i_power=$maxpower;
		}
	}
	if ($in{'kai_wanryoku'}){
		if($in{'kai_wanryoku'} <= 500){
			$i_wanryoku=$in{'kai_wanryoku'};
			$b_wanryoku=int($maxwanryoku/$in{'kai_wanryoku'});
		}else{
			$i_wanryoku=500;
			$b_wanryoku=int($maxwanryoku/500);
		}
	}else{
		if($in{'kai_wanryoku'} eq "0"){
			$i_wanryoku=0;
			$b_wanryoku=$maxwanryoku;
		}else{
			$i_wanryoku=$maxwanryoku;
		}
	}
	if ($in{'kai_kyakuryoku'}){
		if($in{'kai_kyakuryoku'} <= 500){
			$i_kyakuryoku=$in{'kai_kyakuryoku'};
			$b_kyakuryoku=int($maxkyakuryoku/$in{'kai_kyakuryoku'});
		}else{
			$i_kyakuryoku=500;
			$b_kyakuryoku=int($maxkyakuryoku/500);
		}
	}else{
		if($in{'kai_kyakuryoku'} eq "0"){
			$i_kyakuryoku=0;
			$b_kyakuryoku=$maxkyakuryoku;
		}else{
			$i_kyakuryoku=$maxkyakuryoku;
		}
	}
	if ($in{'kai_love'}){
		if($in{'kai_love'} <= 500){
			$i_love=$in{'kai_love'};
			$b_love=int($maxlove/$in{'kai_love'});
		}else{
			$i_love=500;
			$b_love=int($maxlove/500);
		}
	}else{
		if($in{'kai_love'} eq "0"){
			$i_love=0;
			$b_love=$maxlove;
		}else{
			$i_love=$maxlove;
		}
	}
	if ($in{'kai_unique'}){
		if($in{'kai_unique'} <= 500){
			$i_unique=$in{'kai_unique'};
			$b_unique=int($maxunique/$in{'kai_unique'});
		}else{
			$i_unique=500;
			$b_unique=int($maxunique/500);
		}
	}else{
		if($in{'kai_unique'} eq "0"){
			$i_unique=0;
			$b_unique=$maxunique;
		}else{
			$i_unique=$maxunique;
		}
	}
	if ($in{'kai_etti'}){
		if($in{'kai_etti'} <= 500){
			$i_etti=$in{'kai_etti'};
			$b_etti=int($maxetti/$in{'kai_etti'});
		}else{
			$i_etti=500;
			$b_etti=int($maxetti/500);
		}
	}else{
		if($in{'kai_etti'} eq "0"){
			$i_etti=0;
			$b_etti=$maxetti;
		}else{
			$i_etti=$maxetti;
		}
	}
	if ($in{'kai_cal'}){
		if($in{'kai_cal'} <= 99999){
			$i_cal=$in{'kai_cal'};
			$b_cal=int($masyoku/$in{'kai_cal'});
		}else{
			$i_cal=99999;
			$b_cal=int($masyoku/99999);
		}
	}else{
		if($in{'kai_cal'} eq "0"){
			$i_cal=0;
			$b_cal=$maxsyoku;
		}else{
			$i_cal=$maxsyoku;
		}
	}
	if (!$in{'kai_sintai_syouhi'}){$i_sintai_syouhi=0;}else{$i_sintai_syouhi=$in{'kai_sintai_syouhi'};}
	if (!$in{'kai_zunou_syouhi'}){$i_zunou_syouhi=0;}else{$i_zunou_syouhi=$in{'kai_zunou_syouhi'};}
	if ($in{'kai_kankaku'} == 0){$i_kankaku=10;}elsif($in{'kai_kankaku'} <= 1){$i_kankaku=1;}else{$i_kankaku=$in{'kai_kankaku'};} #koko2008/04/12

	$max_mini = 1000;

	if ($b_kokugo && $max_mini >= $b_kokugo){$max_mini = $b_kokugo;}
	if ($b_suugaku && $max_mini >= $b_suugaku){$max_mini = $b_suugaku;}
	if ($b_rika && $max_mini >= $b_rika){$max_mini = $b_rika;}
	if ($b_syakai && $max_mini >= $b_syakai){$max_mini = $b_syakai;}
	if ($b_eigo && $max_mini >= $b_eigo){$max_mini = $b_eigo;}
	if ($b_ongaku && $max_mini >= $b_ongaku){$max_mini = $b_ongaku;}
	if ($b_bijutu && $max_mini >= $b_bijutu){$max_mini = $b_bijutu;}
	if ($b_looks && $max_mini >= $b_looks){$max_mini = $b_looks;}
	if ($b_tairyoku && $max_mini >= $b_tairyoku){$max_mini = $b_tairyoku;}
	if ($b_kenkou && $max_mini >= $b_kenkou){$max_mini = $b_kenkou;}
	if ($b_speed && $max_mini >= $b_speed){$max_mini = $b_speed;}
	if ($b_power && $max_mini >= $b_power){$max_mini = $b_power;}
	if ($b_wanryoku && $max_mini >= $b_wanryoku){$max_mini = $b_wanryoku;}
	if ($b_kyakuryoku && $max_mini >= $b_kyakuryoku){$max_mini = $kyakuryoku;}
	if ($b_love && $max_mini >= $b_love){$max_mini = $b_love;}
	if ($b_unique && $max_mini >= $b_unique){$max_mini = $b_unique;}
	if ($b_etti && $max_mini >= $b_etti){$max_mini = $b_etti;}
	if ($b_cal && $max_mini >= $b_cal){$max_mini = $b_cal;}

	if ($max_mini == 1000){$max_mini =1;}

	$max_taiku = $taiku * $max_mini;

	if (!$in{'kai_zaiko'} || !$in{'kai_taikyuu'}){
		$i_zaiko = 1;
		$i_taikyuu = $max_taiku;
	}elsif ($in{'kai_zaiko'} > $max_taiku){
		$i_zaiko = $max_taiku;
		$i_taikyuu = 1;
	}elsif ($in{'kai_zaiko'} < 1){
		$i_zaiko = 1;
		$i_taikyuu = $max_taiku;
	}elsif ($in{'kai_taikyuu'} < 1){
		$i_zaiko = $max_taiku;
		$i_taikyuu = 1;
	}elsif ($in{'kai_taikyuu'} > $max_taiku){
		$i_zaiko = 1;
		$i_taikyuu = $max_taiku;
	}elsif ($in{'kai_zaiko'}+$in{'kai_taikyuu'} -1  > $max_taiku){
		$i_taikyuu = $in{'kai_taikyuu'};
		$i_zaiko = 1;
	}else{
		$i_zaiko = $in{'kai_zaiko'};
		$i_taikyuu = $in{'kai_taikyuu'};
	}
	if (!$i_zaiko){$i_zaiko = 1;}

	if (!$in{'kai_nedan'}){$i_nedan=$max_taiku * 1000;}else{$i_nedan=$in{'kai_nedan'};}
#koko2007/10/19 ハリス さん提供
	if ($i_nedan < 0){$i_nedan=$max_taiku * 1000;}
	if ($i_nedan > $k_sousisan){$i_nedan=$k_sousisan;}
#end2007/10/19
	$disp_dekiagari = "<input type=\"checkbox\" name=\"dekiagari\" value=\"ok\">生産する。(書き込み)\n";

	&time_get;
	if ($kakou_day ne "$date"){
		if ($in{'dekiagari'}){
			open(OUT,"> ./member/$k_id/itemyou.cgi") || &error("./member/$k_id/itemyou.cgiに書き込めません");
			eval{ flock (OUT, 2); };
			print OUT "$maxkokugo<>$maxsuugaku<>$maxrika<>$maxsyakai<>$maxeigo<>$maxongaku<>$maxbijutu<>$maxlooks<>$maxtairyoku<>$maxkenkou<>$maxspeed<>$maxpower<>$maxwanryoku<>$maxkyakuryoku<>$maxlove<>$maxunique<>$maxetti<>$maxsyoku<>$yo_karada_syou<>$yo_nou_syou<>$taiku<>\n";
			$no++;
			&time_get; #koko2007/12/10
			print OUT "$date<>$i_hinmei（独自製品）<>$no<>$full_date<>\n"; #koko2007/12/10
			close(OUT);

			open(IN,"< ./member/$k_id/omise_log.cgi") || &error("./member/$k_id/omise_log.cgiに読み込めません");
			eval{ flock (IN, 1); };
			@omise = <IN>;
			close(IN);

			$i_time = time;
			push @omise,"$mise_kubun[3]<>$i_hinmei $no<>$i_kokugo<>$i_suugaku<>$i_rika<>$i_syakai<>$i_eigo<>$i_ongaku<>$i_bijutu<>無<>$i_looks<>$i_tairyoku<>$i_kenkou<>$i_speed<>$i_power<>$i_wanryoku<>$i_kyakuryoku<>$i_nedan<>$i_love<>$i_unique<>$i_etti<>$i_taikyuu<>回<>$i_kankaku<>$i_zaiko<>$i_cal<>$i_siyou_date<>$i_sintai_syouhi<>$i_zunou_syouhi<>$i_comment<>$i_time<><><>\n";
			open(OUT,"> ./member/$k_id/omise_log.cgi") || &error("./member/$k_id/omise_log.cgiに書き込めません");
			eval{ flock (OUT, 2); };
			print OUT @omise;
			close(OUT);
			$disp_dekiagari = "本日の生産は完了しました。<br>$full_date\n"; #koko2007/12/10
		}
	}else{
		$disp_dekiagari = "本日の生産は完了しました。<br>$day_tim\n"; #koko2007/12/10
	}

	&time_get;
#	if ($kakou_day ne "$date"){
#	}

	if ($i_kokugo > 500){$i_kokugo = 500;$b_kokugo = int($maxkokugo/500);}
	if ($i_suugaku > 500){$i_suugaku = 500;$b_suugaku = int($maxsuugaku/500);}
	if ($i_rika > 500){$i_rika = 500;$b_rika = int($maxrika/500);}
	if ($i_syakai > 500){$i_syakai = 500;$b_syakai = int($maxsyakai/500);}
	if ($i_eigo > 500){$i_eigo = 500;$b_eigo = int($maxeigo/500);}
	if ($i_ongaku > 500){$i_ongaku = 500;$b_ongaku = int($maxongaku/500);}
	if ($i_bijutu > 500){$i_bijutu = 500;$b_bijutu = int($maxbijutu/500);}
	if ($i_looks > 500){$i_looks = 500;$b_looks = int($maxlooks/500);}
	if ($i_tairyoku > 500){$i_tairyoku = 500;$b_tairyoku = int($maxtairyoku/500);}
	if ($i_kenkou > 500){$i_kenkou = 500;$b_kenkou = int($maxkenkou/500);}
	if ($i_speed > 500){$i_speed = 500;$b_speed = int($maxspeed/500);}
	if ($i_power > 500){$i_power = 500;$b_power = int($maxpower/500);}
	if ($i_wanryoku > 500){$i_wanryoku = 500;$b_wanryoku = int($maxwanryoku/500);}
	if ($i_kyakuryoku > 500){$i_kyakuryoku = 500;$b_kyakuryoku = int($maxkyakuryoku/500);}
	if ($i_love > 500){$i_love = 500;$b_love = int($maxlove/500);}
	if ($i_unique > 500){$i_unique = 500;$b_unique = int($maxunique/500);}
	if ($i_etti > 500){$i_etti = 500;$b_etti = int($maxetti/500);}

	$item_ketasu =3;
	&header(syokudou_style);
	print <<"EOM"; #2007/09/24
<form method="POST" action="$this_script">
<table border="1" cellspacing="1" cellpadding="5" align="center" class="yosumi">
<TR><td>耐久</td><TD><input type="text" size="2" value="$i_taikyuu" name="kai_taikyuu" maxlength="2">$max_taiku = $taiku * $max_mini</TD></TR>
<TR><td>在庫</td><TD><input type="text" size="2" value="$i_zaiko" name="kai_zaiko" maxlength="2">$max_taiku = $taiku * $max_mini</TD></TR>
<TR><TD>種類</td><td>$syu <input type="text" size="20" value="$mise_kubun[3]" name="kai_ty0" maxlength="20"></td></TR>
<TR><TD>品名</td><TD><input type="text" size="50" value="$i_hinmei" name="kai_hinmoku" maxlength="50"></TD></TR>
<TR><TD>備考</td><TD><input type="text" size="50" value="$i_comment" name="kai_comment" maxlength="50"></TD></TR>
<TR><td>国語値</td><TD><input type="text" size="2" value="$i_kokugo" name="kai_kokugo" maxlength="$item_ketasu">$maxkokugo : $b_kokugo</TD></TR>
<TR><td>数学値</td><TD><input type="text" size="2" value="$i_suugaku" name="kai_suugaku" maxlength="$item_ketasu">$maxsuugaku : $b_suugaku</TD></TR>
<TR><td>理科値</td><TD><input type="text" size="2" value="$i_rika" name="kai_rika" maxlength="$item_ketasu">$maxrika : $b_rika</TD></TR>
<TR><td>社会値</td><TD><input type="text" size="2" value="$i_syakai" name="kai_syakai" maxlength="$item_ketasu">$maxsyakai : $b_syakai</TD></TR>
<TR><td>英語値</td><TD><input type="text" size="2" value="$i_eigo" name="kai_eigo" maxlength="$item_ketasu">$maxeigo : $b_eigo</TD></TR>
<TR><td>音楽値</td><TD><input type="text" size="2" value="$i_ongaku" name="kai_ongaku" maxlength="$item_ketasu">$maxongaku : $b_ongaku</TD></TR>
<TR><td>美術値</td><TD><input type="text" size="2" value="$i_bijutu" name="kai_bijutu" maxlength="$item_ketasu">$maxbijutu : $b_bijutu</TD></TR>
<TR><td>ルックス値</td><TD><input type="text" size="2" value="$i_looks" name="kai_looks" maxlength="$item_ketasu">$maxlooks : $b_looks</TD></TR>
<TR><td>体力値</td><TD><input type="text" size="2" value="$i_tairyoku" name="kai_tairyoku" maxlength="$item_ketasu">$maxtairyoku : $b_tairyoku</TD></TR>
<TR><td>健康up値</td><TD><input type="text" size="2" value="$i_kenkou" name="kai_kenkou" maxlength="$item_ketasu">$maxkenkou : $b_kenkou</TD></TR>
<TR><td>スピード値</td><TD><input type="text" size="2" value="$i_speed" name="kai_speed" maxlength="$item_ketasu">$maxspeed : $b_speed</TD></TR>
<TR><td>パワー値</td><TD><input type="text" size="2" value="$i_power" name="kai_power" maxlength="$item_ketasu">$maxpower : $b_power</TD></TR>
<TR><td>腕力値</td><TD><input type="text" size="2" value="$i_wanryoku" name="kai_wanryoku" maxlength="$item_ketasu">$maxwanryoku : $b_wanryoku</TD></TR>
<TR><td>脚力値</td><TD><input type="text" size="2" value="$i_kyakuryoku" name="kai_kyakuryoku" maxlength="$item_ketasu">$maxkyakuryoku : $b_kyakuryoku</TD></TR>
<TR><td>LOVE値</td><TD><input type=text size=2 value="$i_love" name="kai_love" maxlength="$item_ketasu">$maxlove : $b_love</TD></TR>
<TR><td>面白さ値</td><TD><input type="text" size="2" value="$i_unique" name="kai_unique" maxlength="$item_ketasu">$maxunique : $b_unique</TD></TR>
<TR><td>エッチ値</td><TD><input type="text" size="2" value="$i_etti" name="kai_etti" maxlength="$item_ketasu">$maxetti : $b_etti</TD></TR>
<TR><td>カロリー</td><TD><input type="text" size="4" value="$i_cal" name="kai_cal" maxlength="5">$maxsyoku : $b_cal</TD></TR>
<TR><td>身体消費</td><TD><input type="text" size="4" value="$i_sintai_syouhi" name="kai_sintai_syouhi" maxlength="3">0</TD></TR>
<TR><td>頭脳消費</td><TD><input type="text" size="4" value="$i_zunou_syouhi" name="kai_zunou_syouhi" maxlength="3">0</TD></TR>
<TR><td>間隔（分）</td><TD><input type="text" size="3" value="$i_kankaku" name="kai_kankaku" maxlength="2">10</TD></TR>
<TR><td>値段<BR>問屋での価格です</td><TD><input type="text" size="10" value="$i_nedan" name="kai_nedan" maxlength="9">$i_nedan</TD></TR>
<TR><td><br></td><TD>$disp_dekiagari</TD></TR>
</table>
<div align=center><form method=POST action="$this_script">
<input type=hidden name=mode value="seizou">
<input type=hidden name=id value="$k_id">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="変更／作成">
</form></div>
EOM
	&hooter("login_view","街に戻る");

	print "</body></html>\n";

	exit
}

1;
