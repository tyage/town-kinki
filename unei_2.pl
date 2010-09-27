# 運営処理　2007/04/20

# 運営間隔
$unei_time = 1;
# 運営効率
$unei_koritu = 10;
# 総合指数　身長
$unei_yobi5s = "170.0"; #Cm
# 総合指数　体重
$unei_yobi6s = "65.0"; #Kg
# 運営費用
$unei_hiyou = 20000;

# 社員上限  #koko2007/04/29
$syainjougen = 5;

# eval{ flock (UNEI, 2); };
###################################################
sub unei_2 {
#	呼び出し前に  # ($in{'ori_ie_id'},$bangou)が行われている。
	$unei_file="./member/$in{'ori_ie_id'}/$bangou"."_log.cgi"; #koko2007/04/21

	open(UNEI,"$unei_file") || &error("Open Error : $unei_file");
	eval{ flock (UNEI, 2); };
	@all_unei = <UNEI>;
	close(UNEI);

#		$sodate_taisyou_flg=0; #メモ書き
#		foreach (@all_kodomo){
#			if ($unei_num eq $bangou){}
#		}

	($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank)=split(/<>/, $all_unei[0]);
	if (!$ori_ie_rank){return;}

	$in{'ori_ie_id'} = "$in{'ori_ie_id'}".'_'."$bangou";

	if ($in{'command'} eq 'syain_up'){
		push @all_unei,"$unei_num<>$unei_name<><><><>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<><><><>0<>$unei_yobi5<>$unei_yobi6<><>0<><>$ori_ie_rank<>\n";
	}

	$i=0;
	foreach (@all_unei){

		$youikuhi = 0;
		$unei_yobi3 = "";
		$message_in ="";

		($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank)=split(/<>/);

		if (!$unei_yobi5){$unei_yobi5 = $unei_yobi5s;}
		if (!$unei_yobi6){$unei_yobi6 = $unei_yobi6s;}

#パラメータアップの場合
		if ($in{'command'} eq "do_unei" && $in{'syain'} == $i){
#unei_yobi1＝出産時間（秒）unei_yobi2＝最後に子育てした時間　unei_yobi3＝最後の子育てコメント　unei_yobi4＝トータル能力値　unei_yobi5＝身長　unei_yobi6＝体重　unei_yobi7＝最後の食事時間　unei_yobi8＝自立フラグ　unei_yobi9＝最後に子育てした人
		#	if ($in{'unei_num'} eq "$unei_num"){
		#		$sodate_taisyou_flg=1;
			&time_get;
			if (($date_sec - $unei_yobi2) < (60*60*$unei_time)){&error("まだできません。");}

			$konoagatta_suuti = int($in{'par_suuti'}/$unei_koritu);
	
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

			if ($kokugo < 0 || $suugaku < 0 || $rika < 0 || $syakai < 0 || $eigo < 0 || $ongaku < 0 || $bijutu < 0 || $looks < 0 || $tairyoku < 0 || $kenkou < 0 || $speed < 0 || $power < 0 || $wanryoku < 0 || $kyakuryoku < 0 || $love < 0 || $unique < 0 || $etti < 0){&error("パラメータが足りません。親はすべてのパラメータにおいてプラスである必要があります。");}
#最後の子育て時間を更新
			$unei_yobi2 = $date_sec;
	
			$youikuhi = $konoagatta_suuti * $unei_hiyou;
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


		}
#総合能力値計算
		$sogo_sisuu = ($unei_yobi5 + $unei_yobi6)/20;
		$unei_yobi4 = int (($unei_kokugo + $unei_suugaku + $unei_rika + $unei_syakai + $unei_eigo + $unei_ongaku + $unei_bijutu + $unei_looks + $unei_tairyoku + $unei_kenkou + $unei_speed + $unei_power + $unei_wanryoku + $unei_kyakuryoku + $unei_love + $unei_unique + $unei_etti)*$sogo_sisuu);

		
		&jyob_machi2; #koko2007/06/30
		$siokuri_kingaku2 += $siokuri_kingaku1;

		$unei_job = $return_job;
		$unei_yobi8 = 1;

				
		$new_uneiomo_temp0 = "$unei_num<>$unei_name<>$unei_oya1<>$unei_oya2<>$unei_job<>$unei_kokugo<>$unei_suugaku<>$unei_rika<>$unei_syakai<>$unei_eigo<>$unei_ongaku<>$unei_bijutu<>$unei_looks<>$unei_tairyoku<>$unei_kenkou<>$unei_speed<>$unei_power<>$unei_wanryoku<>$unei_kyakuryoku<>$unei_love<>$unei_unique<>$unei_etti<>$unei_yobi1<>$unei_yobi2<>$unei_yobi3<>$unei_yobi4<>$unei_yobi5<>$unei_yobi6<>$unei_yobi7<>$unei_yobi8<>$siokuri_kingaku1<>$ori_ie_rank<>\n";
#	push (@new_all_uneiomo,$new_uneiomo_temp);
#	}	#foreach閉じ
#子供ログ更新
		push @new_uneiomo_temp,$new_uneiomo_temp0;
		if ($syainjougen <= $#new_uneiomo_temp + 1){$#new_uneiomo_temp = $syainjougen - 1;}
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

	&header(assen_style);


		print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●自分の持っているパラメータを社員教育のために使ったりできます。<br>
	●会社は与えたパラメータの$unei_koritu分の1しか得ることができません。<br>
	●会社のパラメータ１に対して$unei_hiyou円の養育費がかかります。<br>
	●社員教育できる間隔は$unei_time時間です。<br>
	●社員総数は、$syainjougen人です。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:24px; color:#ffffff">社員教育</div>
	</td></tr></table><br>
EOM
	if ($unei_name eq $in{'name'}){
		print <<"EOM";
<iframe src="./syokugyo.htm" name="syokugyo" width="90%" height="250px" align=center></iframe>
<table width="90%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td><br></td></tr>
<tr><td>$kokugo</td><td>$suugaku</td><td>$rika</td><td>$syakai</td><td>$eigo</td><td>$ongaku</td><td>$bijutu</td><td>$looks</td><td><br></td></tr>
<tr><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td></tr>
<tr><td>$tairyoku</td><td>$kenkou</td><td>$speed</td><td>$power</td><td>$wanryoku</td><td>$kyakuryoku</td><td>$love</td><td>$unique</td><td>$etti</td></tr></table>
<br><br>
EOM

		$i=0;
		foreach (@all_unei){
			($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank)=split(/<>/);

#持ち物フォーム作成
			print <<"EOM";
<table width="90%" border="0" cellspacing="0" align=center class=yosumi>
<tr bgcolor=#ffffaa><td>
<span class="honbun2">最後の教育：$unei_yobi3</span></td></tr>

<tr bgcolor=#dddddd><td>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="houmon">
<input type=hidden name=command value="do_unei">
<input type=hidden name=ori_ie_id value="$in{'ori_ie_id'}">
<input type=hidden name=unei_num value="$unei_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no value="$in{'town_no'}">
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
</select>
 <select name=par_suuti>
	<option value="1">1</option>
	<option value="2">2</option>
	<option value="3">3</option>
	<option value="5">5</option>
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
<input type=submit value=" あげる ">
</form>
	</td></tr></table>
EOM
			$i++;
			print <<"EOM";
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
	}else{

		foreach (@all_unei){
			($unei_num,$unei_name,$unei_oya1,$unei_oya2,$unei_job,$unei_kokugo,$unei_suugaku,$unei_rika,$unei_syakai,$unei_eigo,$unei_ongaku,$unei_bijutu,$unei_looks,$unei_tairyoku,$unei_kenkou,$unei_speed,$unei_power,$unei_wanryoku,$unei_kyakuryoku,$unei_love,$unei_unique,$unei_etti,$unei_yobi1,$unei_yobi2,$unei_yobi3,$unei_yobi4,$unei_yobi5,$unei_yobi6,$unei_yobi7,$unei_yobi8,$siokuri_kingaku1,$ori_ie_rank)=split(/<>/);
			print <<"EOM";
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
	print "<div align=center><br>総合 $siokuri_kingaku2円<br></div>\n";
	&hooter("login_view","街へ戻る");
exit;
}

#子供自立サブルーチン
sub jyob_machi2 {
	open(SP,"./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 2); };
	my $top_koumoku = <SP>;
	my @job_hairetu = <SP>;
	close(SP);

	$job_name ='';

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
	#	if($unei_yobi5 < $job_sintyou){next;}
		last;
	}	#foreach閉じ
		if ($job_name eq ""){$job_name = "浮浪者";}
		$return_job = $job_name;


		$siokuri_kingaku1 = ($job_kihonkyuu{"$unei_job"} * 10) + ($unei_yobi4 * 10);
		$siokuri_kingaku1 = int ($siokuri_kingaku1 / 4);

}

1;
