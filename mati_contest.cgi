#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。

# eval{ flock (OUT, 2); }; ロック強化 2007/06/19
##############################################
$this_script = 'mati_contest.cgi';
require './town_ini.cgi';
require './town_lib.pl';

# トップタウンだけ投票者分配
$haitoukinitu = 'yes';

# オールタウン投票者分配'yes'
$all_town_touhyounomi = 'no';

# 投票者分配を功労分配にする'yes'
$koroubunpai = 'yes';

# タウンの色分けを使う'yes'
$town_f_color = 'yes';

# タウンカラー('メインタウン色',・・・・)
@town_color = ('#0000ff','#00ff00','#ff00ff','#ff0000');
$i=0;
%town_name_color = ();
foreach (@town_hairetu){
	$town_name_color{"$_"} = $town_color[$i];
	$i++;
}
#=========================
&decode;
#メンテチェック
	if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}
	
$seigenyou_now_time = time;
#制限時間チェック
	$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
	if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#条件分岐
	if($in{'mode'} eq "matikon"){&matikon;}
	elsif($in{'mode'} eq "mati_kouken"){&mati_kouken;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
#############以下サブルーチン
sub matikon {
	open(MA,"< $maticon_logfile") || &error("$maticon_logfileが開けません");
	eval{ flock (MA, 1); };
	$matikon_settei = <MA>;
	@mati_alldata = <MA>;
	close(MA);
	&time_get;
#開始時のログ初期化
	if ($matikon_settei eq ""){
		&lock;
		$i = 0;
		@new_matikon_data = ();
		foreach (@town_hairetu){
			$mati_kon_temp = "$i<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
			if($machikakushi eq 'yes'){ #koko2007/10/21
				unless(($i == $kakushimachi_no && $kakushimachi_no) || ($i == $kakushimachi_no1 && $kakushimachi_no1) || ($i == $kakushimachi_no2 && $kakushimachi_no2) || ($i == $kakushimachi_no3 && $kakushimachi_no3) || ($i == $kakushimachi_no4 && $kakushimachi_no4) ){
					push (@new_matikon_data,$mati_kon_temp);
				}
			}else{ #koko2007/10/21 #koko2008/05/04
				push (@new_matikon_data,$mati_kon_temp);
			}#end2008/05/04
			$i ++;
		}
		@mati_alldata = @new_matikon_data;
		$matikon_settei = "$date_sec<>1<>1<>\n";
		unshift (@new_matikon_data,$matikon_settei);
		open(OUT,">$maticon_logfile") || &error("Open Error : $maticon_logfile");
		eval{ flock (OUT, 2); };
		print OUT @new_matikon_data;
		close(OUT);
		&unlock;
	}
#新しく街を追加した場合、街データに追加
	$i = 0;
	$tuika_flag=0;
	foreach (@town_hairetu){
		my $new_mati_hueta = 0;
		foreach $kizon_mati (@mati_alldata){
			($mat_num) = split(/<>/,$kizon_mati);
			if ($mat_num eq $i){$new_mati_hueta = 1;}
		}
		if ($new_mati_hueta == 0){		#街データに無い街番号（街配列が見つかった場合）
			my $mati_kon_temp = "$i<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>\n";
			if($machikakushi eq 'yes'){ #koko2007/10/21
				unless(($i == $kakushimachi_no && $kakushimachi_no) || ($i == $kakushimachi_no1 && $kakushimachi_no1) || ($i == $kakushimachi_no2 && $kakushimachi_no2) || ($i == $kakushimachi_no3 && $kakushimachi_no3) || ($i == $kakushimachi_no4 && $kakushimachi_no4) ){
					push (@mati_alldata,$mati_kon_temp);
				}
			}else{ #end2007/10/21 #koko2008/05/04
				push (@mati_alldata,$mati_kon_temp);
			}#end2008/05/04
			$tuika_flag=1;

		}
		$i ++;
	}
	if ($tuika_flag ==1){
		&lock;
		unshift (@mati_alldata,$matikon_settei);
		open(OUT,">$maticon_logfile") || &error("Open Error : $maticon_logfile");
		eval{ flock (OUT, 2); };
		print OUT @mati_alldata;
		close(OUT);
		&unlock;
		shift  @mati_alldata;
	}

#設定行読み込み、何大会何日目設定
	$saisyuu_flag=0;
	($start_con_time,$nannitime_hozon,$dainankai_con,$rank_hiduke)= split(/<>/,$matikon_settei);
	$nannitime_con = int(($date_sec - $start_con_time) / (60*60*24)) + 1;
	if ($nannitime_con ne "$nannitime_hozon" && $nannitime_con <= $mati_con_nissuu){&matikon_changeDay;}
	if ($nannitime_con > $mati_con_nissuu){&matikon_saisyuu;}
	if ($nannitime_con == $mati_con_nissuu){
		$nanniti_hyouki = "最終日";
	}else{
		$nanniti_hyouki = "$nannitime_con日目";
	}
#ランキングソート
	@matirank_alldata = (@mati_alldata); #koko2007/07/18 2008/05/03
#	foreach (@mati_alldata){
#		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$mat_yobi2,$mat_yobi3,$mat_yobi4,$mat_yobi5)= split(/<>/);
#		$data=$_;
#		$bunka_key=(split(/<>/,$data))[5];
#		$sports_key=(split(/<>/,$data))[6];
#		$ninjou_key=(split(/<>/,$data))[7];
#		$yuuhuku_key=(split(/<>/,$data))[8];
#		$bunka_z_key=(split(/<>/,$data))[9];
#		$sports_z_key=(split(/<>/,$data))[10];
#		$ninjou_z_key=(split(/<>/,$data))[11];
#		$yuuhuku_z_key=(split(/<>/,$data))[12];
	#	push @matirank_alldata,$data;
#		push @bunkaKeys,$bunka_key;
#		push @sportsKeys,$sports_key;
#		push @ninjouKeys,$ninjou_key;
#		push @yuuhukuKeys,$yuuhuku_key;
#		push @bunka_zKeys,$bunka_z_key;
#		push @sports_zKeys,$sports_z_key;
#		push @ninjou_zKeys,$ninjou_z_key;
#		push @yuuhuku_zKeys,$yuuhuku_z_key;
#	}
#	sub bybunkaKeys{$bunkaKeys[$b] <=> $bunkaKeys[$a];}
#	@bunka_rank=@matirank_alldata[ sort bybunkaKeys 0..$#matirank_alldata]; 

	@bunkaKeys = map {(split /<>/)[5]} @matirank_alldata;
	@bunka_rank = @matirank_alldata[sort {@bunkaKeys[$b] <=> @bunkaKeys[$a]} 0 .. $#bunkaKeys];


#	sub bysportsKeys{$sportsKeys[$b] <=> $sportsKeys[$a];}
#	@sports_rank=@matirank_alldata[ sort bysportsKeys 0..$#matirank_alldata]; 

	@sportsKeys = map {(split /<>/)[6]} @matirank_alldata;
	@sports_rank = @matirank_alldata[sort {@sportsKeys[$b] <=> @sportsKeys[$a]} 0 .. $#sportsKeys];

#	sub byninjouKeys{$ninjouKeys[$b] <=> $ninjouKeys[$a];}
#	@ninjou_rank=@matirank_alldata[ sort byninjouKeys 0..$#matirank_alldata]; 

	@ninjouKeys = map {(split /<>/)[7]} @matirank_alldata;
	@ninjou_rank = @matirank_alldata[sort {@ninjouKeys[$b] <=> @ninjouKeys[$a]} 0 .. $#ninjouKeys];

#	sub byyuuhukuKeys{$yuuhukuKeys[$b] <=> $yuuhukuKeys[$a];}
#	@yuuhuku_rank=@matirank_alldata[ sort byyuuhukuKeys 0..$#matirank_alldata]; 

	@yuuhukuKeys = map {(split /<>/)[8]} @matirank_alldata;
	@yuuhuku_rank = @matirank_alldata[sort {@yuuhukuKeys[$b] <=> @yuuhukuKeys[$a]} 0 .. $#yuuhukuKeys];

#	sub bybunka_zKeys{$bunka_zKeys[$b] <=> $bunka_zKeys[$a];}
#	@bunka_z_rank=@matirank_alldata[ sort bybunka_zKeys 0..$#matirank_alldata]; 

	@bunka_zKeys = map {(split /<>/)[9]} @matirank_alldata;
	@bunka_z_rank = @matirank_alldata[sort {@bunka_zKeys[$b] <=> @bunka_zKeys[$a]} 0 .. $#bunka_zKeys];

#	sub bysports_zKeys{$sports_zKeys[$b] <=> $sports_zKeys[$a];}
#	@sports_z_rank=@matirank_alldata[ sort bysports_zKeys 0..$#matirank_alldata]; 

	@sports_zKeys = map {(split /<>/)[10]} @matirank_alldata;
	@sports_z_rank = @matirank_alldata[sort {@sports_zKeys[$b] <=> @sports_zKeys[$a]} 0 .. $#sports_zKeys];

#	sub byninjou_zKeys{$ninjou_zKeys[$b] <=> $ninjou_zKeys[$a];}
#	@ninjou_z_rank=@matirank_alldata[ sort byninjou_zKeys 0..$#matirank_alldata]; 

	@ninjou_zKeys = map {(split /<>/)[11]} @matirank_alldata;
	@ninjou_z_rank = @matirank_alldata[sort {@ninjou_zKeys[$b] <=> @ninjou_zKeys[$a]} 0 .. $#ninjou_zKeys];

#	sub byyuuhuku_zKeys{$yuuhuku_zKeys[$b] <=> $yuuhuku_zKeys[$a];}
#	@yuuhuku_z_rank=@matirank_alldata[ sort byyuuhuku_zKeys 0..$#matirank_alldata]; 

	@yuuhuku_zKeys = map {(split /<>/)[12]} @matirank_alldata;
	@yuuhuku_z_rank = @matirank_alldata[sort {@yuuhuku_zKeys[$b] <=> @yuuhuku_zKeys[$a]} 0 .. $#yuuhuku_zKeys];
#kokoend2006/03/12

	&header(gym_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>$titleが運営する「街コンテスト」です。自分の持っているパラーメータ値やお金を自分の住んでいる街のために使うことで、「文化度」「スポーツ振興度」「人気度」「裕福度」の各街パラメーターが上がります。<br>前日までの街パラメーターの多さによって翌日、順位が確定されます。<br>
$mati_con_nissuu日間が過ぎた時点で最終的な順位が決定し、それぞれのランキングごとに優勝賞金が街に与えられます（４つのランキングすべてで優勝すれば下記賞金×４となります）。それを住民で山分けした額が普通口座に振り込まれます。<br>街の名誉を賭けて頑張りましょう。<br>
※各ランキングの優勝賞金：$mati_con_syoukin万円<br>
※自分の家を持っていない方はこのコンテストに参加することはできません。パラメーターをあげられる間隔は１時間です。</td>
<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>街コンテスト</b></font></td>
<div style="color:ffffff; font-size:14px;">第$dainankai_con回大会</div>
<div style="color:ffff66; font-size:13px;">$nanniti_hyouki</div>
</td>
</tr></table><br>
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td colspan=4>
<div class=tyuu>現在のランキング（$rank_hiduke集計）</div>
</td></tr>
<tr align=center><td>
<table border="0" cellspacing="1" cellpadding="3" ><tr><td colspan=3>■文化度</td></tr>
<tr class=jouge bgcolor=#ffff66 align=center><td></td><td>街　名</td><td>ポイント</td></tr>
EOM
	$i = 1;
	foreach (@bunka_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if (($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) ||($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4) ){next;}
		} #end2007/10/21

		if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
		print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_bunka_y</td></tr>";
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" ><tr><td colspan=3>■スポーツ振興度</td></tr>
<tr class=jouge  bgcolor=#ffff66 align=center><td></td><td>街　名</td><td>ポイント</td></tr>
EOM
	$i = 1;
	foreach (@sports_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if (($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) ||($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4) ){next;}
		} #end2007/10/21
		if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
		print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_sports_y</td></tr>";
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" ><tr><td colspan=3>■人気度</td></tr>
<tr class=jouge bgcolor=#ffff66 align=center><td></td><td>街　名</td><td>ポイント</td></tr>
EOM
	$i = 1;
	foreach (@ninjou_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if (($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) ||($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4) ){next;}
		}#end2007/10/21
		if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
		print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_ninjou_y</td></tr>";
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" ><tr><td colspan=3>■裕福度</td></tr>
<tr class=jouge bgcolor=#ffff66 align=center><td></td><td>街　名</td><td>寄付金額</td></tr>
EOM

	$i = 1;
	foreach (@yuuhuku_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if ($machikakushi eq 'yes'){ #koko2007/10/21
			if(($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) || ($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4)){next;}
		} #end2007/10/21
		if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
		print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_yuuhuku_y円</td></tr>";
		$i ++;
	}
	
	print <<"EOM";
</table>
</td></tr></table><br><br>
EOM
#功労者ランキングの出力
	print <<"EOM";
<table width="90%" border="0" cellspacing="1" cellpadding="3" align=center class=yosumi>
<tr><td colspan=5>
<div class=tyuu>現在の功労者ランキングベスト5</div>
※「貢献度」は各貢献ポイントの合計です。寄付金は１万１ポイントで計算。
</td></tr>
<tr class=jouge bgcolor=#ffcc99 align=center><td></td><td>名前</td><td>貢献度</td><td>文化貢献</td><td>スポーツ貢献</td><td>人気貢献</td><td>寄付金</td></tr>
EOM
	open(KOR,"< $kourousya_logfile") || &error("$kourousya_logfileが開けません");
	eval{ flock (KOR, 1); };
	@kourou_alldata = <KOR>;
	close(KOR);
	@kourou_alldata0 = (@kourou_alldata);
#koko2006/03/12
#	foreach (@kourou_alldata){
#		$data=$_;
#		$kourou_key=(split(/<>/,$data))[2];
#		$kourou_z_key=(split(/<>/,$data))[12];
#		push @korourank_alldata,$data;
#		push @kourouKeys,$kourou_key;
#		push @kourou_zKeys,$kourou_z_key;
#	}
		@korourank_alldata = (@kourou_alldata);

#		sub bykourouKeys{$kourouKeys[$b] <=> $kourouKeys[$a];}
#		@kourou_rank=@korourank_alldata[ sort bykourouKeys 0..$#korourank_alldata]; 

		@kourouKeys = map {(split /<>/)[2]} @korourank_alldata;
		@kourou_rank = @korourank_alldata[sort {@kourouKeys[$b] <=> @kourouKeys[$a]} 0 .. $#kourouKeys];
		
#		sub bykourou_zKeys{$kourou_zKeys[$b] <=> $kourou_zKeys[$a];}
#		@kourou_z_rank=@korourank_alldata[ sort bykourou_zKeys 0..$#korourank_alldata]; 

		@kourou_zKeys = map {(split /<>/)[12]} @korourank_alldata;
		@kourou_z_rank = @korourank_alldata[sort {@kourou_zKeys[$b] <=> @kourou_zKeys[$a]} 0 .. $#kourou_zKeys];
#kokoend2006/03/12

	$i = 1;
	foreach (@kourou_rank){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
#kourou_yobi1 = 最終貢献時間　kourou_yobi2＝kourou_total_z（前回の功労ポイントトータル）kourou_yobi3 = 累積功労トータル
		if($town_f_color eq 'yes'){$town_name_disp = "<font color=\"$town_name_color{\"$kourou_yobi4\"}\">$kourou_name</font>"}else{$town_name_disp = "$kourou_name($kourou_yobi4)";}
		print "<tr align=right><td>$i位</td><td align=left>$town_name_disp</td><td>$kourou_totalポイント</td><td>$kourou_bunka</td><td>$kourou_sports</td><td>$kourou_ninjou</td><td>$kourou_yuuhuku円</td></tr>";
		if($i >= 5){last;}
		$i ++;
	}
	print "</table><br><br>";
	$now_time = time;
	foreach (@kourou_rank){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
		if($name eq $kourou_name){
			if($kourou_yobi1+(60*60) > $now_time){
				$mati_time = int(($kourou_yobi1+(60*60)-$now_time)/60) ."分".($kourou_yobi1+(60*60)-$now_time)%60 ."秒 お待ちください";
			}
			last;
		}
	}

	if($mati_time){

		print "<div class=honbun2 align=center>$nameさんは $mati_time</div>";

	}else{
		&my_town_check($name);
#家を持っている人用の出力
		if ($return_my_town ne "no_town"){
			print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td colspan=2>
<div class=tyuu>自分の街（$town_hairetu[$return_my_town]）へ貢献する</div>
※１回の貢献では、パラメーター、あるいはお金、どちらかひとつだけをあげることができます。間隔は1時間です。<br>
あなたは$kourou_totalポイント　文化貢献：$kourou_bunka　スポーツ貢献：$kourou_sports　人気貢献：$kourou_ninjou　寄付金：$kourou_yuuhuku円です。
</td></tr>
<tr><td width=50%>
<form method=POST action="$this_script">
<input type=hidden name=mode value="mati_kouken">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=sunderu_mati value="$return_my_town">
●パラメーターアップ<br>
<select name=nouryoku>
<optgroup label="文化">
<option value="kokugo">国語</option>
<option value="suugaku">数学</option>
<option value="rika">理科</option>
<option value="syakai">社会</option>
<option value="eigo">英語</option>
<option value="ongaku">音楽</option>
<option value="bijutu">美術</option>
</optgroup>
<optgroup label="スポーツ振興">
<option value="tairyoku">体力</option>
<option value="kenkou">健康</option>
<option value="speed">スピード</option>
<option value="power">パワー</option>
<option value="wanryoku">腕力</option>
<option value="kyakuryoku">脚力</option>
</optgroup>
<optgroup label="人気">
<option value="looks">ルックス</option>
<option value="love">LOVE</option>
<option value="unique">面白さ</option>
<option value="etti">エッチ</option>
</optgroup>
</select>
<select name=suuti>
<option value="5">5ポイント</option>
<option value="10">10ポイント</option>
<option value="15">15ポイント</option>
<option value="20">20ポイント</option>
<option value="25">25ポイント</option>
<option value="30">30ポイント</option>
<option value="40">40ポイント</option>
<option value="50">50ポイント</option>
</select>
<input type=submit value=" O K ">
</form>
</td><td>
<form method=POST action="$this_script">
<input type=hidden name=mode value="mati_kouken">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=sunderu_mati value="$return_my_town">
●裕福度アップ<br>
<select name=okane>
<option value="">金額の選択</option>
<option value="10000">1万円</option>
<option value="30000">3万円</option>
<option value="50000">5万円</option>
<option value="100000">10万円</option>
<option value="200000">20万円</option>
<option value="300000">30万円</option>
<option value="400000">40万円</option>
<option value="500000">50万円</option>
</select>
<input type=submit value=" O K ">
</form>
</td></tr></table>
EOM
#家がない人用の出力
		}else{
			print "<div class=honbun2 align=center>$nameさんは家を持っていないので街への貢献はできません。</div>";
		}
	}
#前回最終ランキング
	$zenkai_taikai = $dainankai_con-1;
	if ($zenkai_taikai != 0){
	print <<"EOM";
<br><br><table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td colspan=4>
<div class=tyuu>第$zenkai_taikai回大会最終順位</div>
</td></tr>
<tr align=center><td>
<table border="0" cellspacing="1" cellpadding="3">
EOM
	$i = 1;
	foreach (@bunka_z_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if(($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) || ($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4)){next;}
		} #end2007/10/21
		if ($i == 1){
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr align=center bgcolor=#ffff66 class=jouge><td colspan=3>文化度<div class=tyuu>優勝</div><div class=dai>$town_font_color</div>（$mat_bunka_zポイント）</td></tr>";
			if($saisyuu_flag ==1 && $mat_num == 0 && ($haitoukinitu eq 'yes' || $all_town_touhyounomi eq 'yes')){&syoukin_haihu_sanka($mat_num,"（文化度）");}
			elsif($saisyuu_flag ==1){&syoukin_haihu($mat_num,"（文化度）");}
		}else{
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_bunka_z</td></tr>";
		}
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" >
EOM
	$i = 1;
	foreach (@sports_z_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if(($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) || ($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4)){next;}
		} #end2007/10/21
		if ($i == 1){
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr align=center bgcolor=#ffff66 class=jouge><td colspan=3>スポーツ振興度<div class=tyuu>優勝</div><div class=dai>$town_font_color</div>（$mat_sports_zポイント）</td></tr>";
			if($saisyuu_flag ==1 && $mat_num == 0 && ($haitoukinitu eq 'yes' || $all_town_touhyounomi eq 'yes')){&syoukin_haihu_sanka($mat_num,"（スポーツ振興度）");}
			elsif($saisyuu_flag ==1){&syoukin_haihu($mat_num,"（スポーツ振興度）");}
		}else{
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr><td>$i位</td><td>$town_font_color</td><td align=right>$mat_sports_z</td></tr>";
		}
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" >
EOM
	$i = 1;
	foreach (@ninjou_z_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if(($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) || ($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4)){next;}
		} #end2007/10/21
		if ($i == 1){
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr align=center bgcolor=#ffff66 class=jouge><td colspan=3>人気度<div class=tyuu>優勝</div><div class=dai>$town_font_color</div>（$mat_ninjou_zポイント）</td></tr>";
			if($saisyuu_flag ==1 && $mat_num == 0 && ($haitoukinitu eq 'yes' || $all_town_touhyounomi eq 'yes')){&syoukin_haihu_sanka($mat_num,"（人気度）");}
			elsif($saisyuu_flag ==1){&syoukin_haihu($mat_num,"（人気度）");}
		}else{
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_ninjou_z</td></tr>";
		}
		$i ++;
	}
	print <<"EOM";
</table>
</td><td>
<table border="0" cellspacing="1" cellpadding="3" >
EOM

	$i = 1;
	foreach (@yuuhuku_z_rank){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$k_yobi2,$k_yobi3,$k_yobi4,$k_yobi5)= split(/<>/);
		if($machikakushi eq 'yes'){ #koko2007/10/21
			if(($mat_num eq $kakushimachi_no && $kakushimachi_no) || ($mat_num eq $kakushimachi_no1 && $kakushimachi_no1) || ($mat_num eq $kakushimachi_no2 && $kakushimachi_no2) || ($mat_num eq $kakushimachi_no3 && $kakushimachi_no3) || ($mat_num eq $kakushimachi_no4 && $kakushimachi_no4)){next;}
		} #end2007/10/21
		if ($i == 1){
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr align=center bgcolor=#ffff66 class=jouge><td colspan=3>裕福度<div class=tyuu>優勝</div><div class=dai>$town_font_color</div>（$mat_yuuhuku_z円）</td></tr>";
			if($saisyuu_flag ==1 && $mat_num == 0 && ($haitoukinitu eq 'yes' || $all_town_touhyounomi eq 'yes')){&syoukin_haihu_sanka($mat_num,"（裕福度）");}
			elsif($saisyuu_flag ==1){&syoukin_haihu($mat_num,"（裕福度）");}
		}else{
			if($town_f_color eq 'yes'){$town_font_color = "<font color=\"$town_color[$mat_num]\"}\">$town_hairetu[$mat_num]</font>"}else{$town_font_color = "$town_hairetu[$mat_num]";}
			print "<tr><td>$i</td><td>$town_font_color</td><td align=right>$mat_yuuhuku_z円</td></tr>";
		}
		$i ++;
	}
	
	print <<"EOM";
</table>
</td></tr></table><br><br>
EOM

#前回功労者ランキングの出力
	print <<"EOM";
<table width="90%" border="0" cellspacing="1" cellpadding="3" align=center  class=yosumi>
<tr><td colspan=5>
<div class=tyuu>第$zenkai_taikai回大会功労者ランキングベスト10</div>
</td></tr>
<tr class=jouge bgcolor=#ffcc99 align=center><td></td><td>名前</td><td>貢献度</td><td>文化貢献</td><td>スポーツ貢献</td><td>人気貢献</td><td>寄付金</td></tr>
EOM
	$i = 1;
	foreach (@kourou_z_rank){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
#kourou_yobi1 = 最終貢献時間　kourou_yobi2＝kourou_total_z（前回の功労ポイントトータル）kourou_yobi3 = 累積功労トータル
#$kourou_yobi4 = 街番号
	#	if($kourou_yobi4 ne ""){$mache_name = $kourou_yobi4;}
		if($town_f_color eq 'yes'){$town_name_disp = "<font color=\"$town_name_color{\"$kourou_yobi4\"}\">$kourou_name</font>"}else{$town_name_disp = "$kourou_name($kourou_yobi4)";}
		print "<tr align=right><td>$i位</td><td align=left>$town_name_disp</td><td>$kourou_yobi2ポイント</td><td>$kourou_bunka_z</td><td>$kourou_sports_z</td><td>$kourou_ninjou_z</td><td>$kourou_yuuhuku_z円</td></tr>";
		if($i >= 10){last;}
		$i ++;
	}
	print "</table><br><br>";
	}		#前回大会が0でなかったらの閉じ
	&hooter("login_view","戻る");
	exit;
}

###街の貢献処理
sub mati_kouken {
	if ($in{'nouryoku'} eq "" && $in{'okane'} eq ""){&error("貢献する内容が選ばれていません");}
#功労者ファイルへの書き込み
	open(KOR,"< $kourousya_logfile") || &error("$kourousya_logfileが開けません");
	eval{ flock (KOR, 1); };
	@kourou_alldata = <KOR>;
	close(KOR);
	$kourou_member_flag = 0;
	my $now_time = time;

	if ($in{'suuti'} < 0){&error("マイナスの数値は受け付けられません。");} #koko2007/07/18
	if ($in{'okane'} < 0){&error("マイナスのお金は受け付けられません。");} #koko2007/07/18
#koko2007/10/19 ハリス さん指摘
	if ($in{'suuti'}){
		if ($in{'suuti'} > 50 || $in{'suuti'} < 5){&error("不正な操作です。");}
	}
	if ($in{'okane'}){
		if ($in{'okane'} > 500000 || $in{'okane'} < 1000){&error("不正な操作です。");}
	}
#end2007/10/19
	&my_town_check($name);

	@new_kourou_alldata = (); #koko2007/07/18

	foreach (@kourou_alldata){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);

		if($kourou_yobi1 < $now_time - ($mati_con_nissuu * 2)*24*60*60){next;}

		if ($name eq $kourou_name){
			if($now_time - $kourou_yobi1 < 60*60){&error("貢献できる間隔の１時間がまだ経過していません");}
			$kourou_member_flag = 1;
			$kourou_yobi1 = $now_time;	#最終貢献時間を記録
			if ($in{'nouryoku'}){		#パラメータアップの場合
				$kourou_total += $in{'suuti'};
				if ($in{'nouryoku'} eq "kokugo" || $in{'nouryoku'} eq "suugaku" || $in{'nouryoku'} eq "rika" || $in{'nouryoku'} eq "syakai" || $in{'nouryoku'} eq "eigo" || $in{'nouryoku'} eq "ongaku" || $in{'nouryoku'} eq "bijutu"){		#文化貢献
					$kourou_bunka += $in{'suuti'};
					
				}elsif($in{'nouryoku'} eq "tairyoku" || $in{'nouryoku'} eq "kenkou" || $in{'nouryoku'} eq "speed" || $in{'nouryoku'} eq "power" || $in{'nouryoku'} eq "wanryoku" || $in{'nouryoku'} eq "kyakuryoku"){		#スポーツ貢献
					$kourou_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "looks" || $in{'nouryoku'} eq "love" || $in{'nouryoku'} eq "unique" || $in{'nouryoku'} eq "etti"){		#人気貢献
					$kourou_ninjou += $in{'suuti'};
				}
			}elsif($in{'okane'}){		#寄付金の場合
				if ($money <= $in{'okane'}){&error("お金が足りません");}
				$okane_kanzan = $in{'okane'}/10000;
				$kourou_total += $okane_kanzan;
				$kourou_yuuhuku += $in{'okane'};
			}

			$kourou_yobi4 = $town_hairetu[$return_my_town];
			$kourou_id = $k_id;

		}		#名前一致の場合の閉じ
		$kourou_temp = "$kourou_id<>$kourou_name<>$kourou_total<>$kourou_bunka<>$kourou_sports<>$kourou_ninjou<>$kourou_yuuhuku<>$kourou_bunka_z<>$kourou_sports_z<>$kourou_ninjou_z<>$kourou_yuuhuku_z<>$kourou_yobi1<>$kourou_yobi2<>$kourou_yobi3<>$kourou_yobi4<>$kourou_yobi5<>\n";
		push (@new_kourou_alldata,$kourou_temp);
	}		#foreachの閉じ
#新規功労者の場合
	if ($kourou_member_flag == 0){
	#	$kourou_num ++;
		if ($in{'okane'}){
			$n_kourou_total += $in{'okane'}/10000;
			$n_kourou_yuuhuku += $in{'okane'};
			$n_kourou_bunka = 0; $n_kourou_sports = 0; $n_kourou_ninjou = 0;
		}else{
			$n_kourou_total += $in{'suuti'};
			if ($in{'nouryoku'} eq "kokugo" || $in{'nouryoku'} eq "suugaku" || $in{'nouryoku'} eq "rika" || $in{'nouryoku'} eq "syakai" || $in{'nouryoku'} eq "eigo" || $in{'nouryoku'} eq "ongaku" || $in{'nouryoku'} eq "bijutu"){		#文化貢献
				$n_kourou_bunka = $in{'suuti'};$n_kourou_sports = 0;$n_kourou_ninjou = 0;$n_kourou_yuuhuku = 0;
			}elsif($in{'nouryoku'} eq "tairyoku" || $in{'nouryoku'} eq "kenkou" || $in{'nouryoku'} eq "speed" || $in{'nouryoku'} eq "power" || $in{'nouryoku'} eq "wanryoku" || $in{'nouryoku'} eq "kyakuryoku"){		#スポーツ貢献
				$n_kourou_sports = $in{'suuti'};$n_kourou_bunka = 0;$n_kourou_ninjou = 0;$n_kourou_yuuhuku = 0;
			}elsif($in{'nouryoku'} eq "looks" || $in{'nouryoku'} eq "love" || $in{'nouryoku'} eq "unique" || $in{'nouryoku'} eq "etti"){		#人気貢献
				$n_kourou_ninjou = $in{'suuti'};$n_kourou_sports = 0;$n_kourou_bunka = 0;$n_kourou_yuuhuku = 0;
			}
		}
		
		$sinki_kourou_temp = "$k_id<>$name<>$n_kourou_total<>$n_kourou_bunka<>$n_kourou_sports<>$n_kourou_ninjou<>$n_kourou_yuuhuku<>0<>0<>0<>0<>$now_time<>0<>0<>$town_hairetu[$return_my_town]<>0<>\n";
		push (@new_kourou_alldata,$sinki_kourou_temp);
	}
	
#街ファイルへの書き込み＆個人パラメータを引く
	open(MA,"< $maticon_logfile") || &error("$maticon_logfileが開けません");
	eval{ flock (MA, 1); };
	$matikon_settei = <MA>;
	@mati_alldata = <MA>;
	close(MA);
	@new_mati_alldata = (); #koko2007/07/18
	foreach (@mati_alldata){
		($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$mat_yobi2,$mat_yobi3,$mat_yobi4,$mat_yobi5)= split(/<>/);
#自分の街だった場合
		if ($in{'sunderu_mati'} eq "$mat_num"){
#パラメータアップの場合
			if ($in{'nouryoku'}){
				if ($in{'nouryoku'} eq "kokugo"){
					$kokugo -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "suugaku"){
					$suugaku -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "rika"){
					$rika -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "syakai"){
					$syakai -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "eigo"){
					$eigo -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "ongaku"){
					$ongaku -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "bijutu"){
					$bijutu -= $in{'suuti'};
					$mat_bunka += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "tairyoku"){
					$tairyoku -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "kenkou"){
					$kenkou -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "speed"){
					$speed -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "power"){
					$power -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "wanryoku"){
					$wanryoku -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "kyakuryoku"){
					$kyakuryoku -= $in{'suuti'};
					$mat_sports += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "looks"){
					$looks -= $in{'suuti'};
					$mat_ninjou += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "love"){
					$love -= $in{'suuti'};
					$mat_ninjou += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "unique"){
					$unique -= $in{'suuti'};
					$mat_ninjou += $in{'suuti'};
				}elsif($in{'nouryoku'} eq "etti"){
					$etti -= $in{'suuti'};
					$mat_ninjou += $in{'suuti'};
				}
#寄付金の場合
			}elsif ($in{'okane'}){
				$money -= $in{'okane'};
				$mat_yuuhuku += $in{'okane'};
			}			#裕福度アップの場合の閉じ
		}		#自分の街だった場合の閉じ
		my $kouken_temp = "$mat_num<>$mat_bunka<>$mat_sports<>$mat_ninjou<>$mat_yuuhuku<>$mat_bunka_y<>$mat_sports_y<>$mat_ninjou_y<>$mat_yuuhuku_y<>$mat_bunka_z<>$mat_sports_z<>$mat_ninjou_z<>$mat_yuuhuku_z<>$mat_yobi1<>$mat_yobi2<>$mat_yobi3<>$mat_yobi4<>$mat_yobi5<>\n";
		push (@new_mati_alldata,$kouken_temp);
	}			#foreachの閉じ
	unshift (@new_mati_alldata,$matikon_settei);
#koko2008/04/08
	@kourou_zKeys = map {(split /<>/)[12]} @new_kourou_alldata;
	@new_kourou_alldata = @new_kourou_alldata[sort {@kourou_zKeys[$b] <=> @kourou_zKeys[$a]} 0 .. $#kourou_zKeys];

#ログ更新
			&lock;
	open(KOO,">$kourousya_logfile") || &error("$kourousya_logfileに書き込めません");
	eval{ flock (KOO, 2); };
	print KOO @new_kourou_alldata;
	close(KOO);
			
	open(MK,">$maticon_logfile") || &error("$maticon_logfileに書き込めません");
	eval{ flock (MK, 2); };
	print MK @new_mati_alldata;
	close(MK);
	&unlock;
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&header("","sonomati");
	print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>街への貢献をしました。このポイントは次回のランキング集計時に反映されます。</td></tr></table><br>
<form method=POST action="$this_script">
<input type=hidden name=mode value="matikon">
<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=admin_pass value="$in{'admin_pass'}">
<input type=submit value="戻る">
</form></div>
</body></html>
EOM
exit;
}

#日付変更処理（昨日時点の数値を移動）
sub matikon_changeDay {
	&lock;
	@change_mati_alldata = (); #koko2007/07/18
	foreach (@mati_alldata){
		my ($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$mat_yobi2,$mat_yobi3,$mat_yobi4,$mat_yobi5)= split(/<>/);
		$mat_bunka_y = $mat_bunka;
		$mat_sports_y = $mat_sports;
		$mat_ninjou_y = $mat_ninjou;
		$mat_yuuhuku_y = $mat_yuuhuku;
		$changeDay_temp = "$mat_num<>$mat_bunka<>$mat_sports<>$mat_ninjou<>$mat_yuuhuku<>$mat_bunka_y<>$mat_sports_y<>$mat_ninjou_y<>$mat_yuuhuku_y<>$mat_bunka_z<>$mat_sports_z<>$mat_ninjou_z<>$mat_yuuhuku_z<>$mat_yobi1<>$mat_yobi2<>$mat_yobi3<>$mat_yobi4<>$mat_yobi5<>\n";
		push (@change_mati_alldata,$changeDay_temp);
	}
	@mati_alldata = ();
	@mati_alldata = @change_mati_alldata;
	$nannitime_hozon = $nannitime_con ;
	$rank_hiduke = "$date2";
	$change_matikon_settei = "$start_con_time<>$nannitime_hozon<>$dainankai_con<>$rank_hiduke<>\n";
	unshift (@change_mati_alldata,$change_matikon_settei);
	open(OUT,">$maticon_logfile") || &error("Open Error : $maticon_logfile");
	eval{ flock (OUT, 2); };
	print OUT @change_mati_alldata;
	close(OUT);
	&unlock;
}


#住んでいる街のチェックサブルーチン
sub my_town_check {
	open(MTC,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (MTC, 1); };
	my @ori_ie_para = <MTC>;
	close(MTC);
	$my_town_ari = 0;
	foreach (@ori_ie_para){
		my ($ori_k_id,$ori_ie_name,$ori_ie_setumei,$ori_ie_image,$ori_ie_syubetu,$ori_ie_kentikubi,$ori_ie_town)= split(/<>/);
		if (@_[0] eq "$ori_ie_name"){
			$return_my_town = "$ori_ie_town";
			$my_town_ari = 1;
			last;
		}
	}
	if ($my_town_ari == 0){$return_my_town = "no_town";}
}

#最終ランキング処理
sub matikon_saisyuu {
	&lock;
	@change_mati_alldata = ();
	foreach (@mati_alldata){
		my ($mat_num,$mat_bunka,$mat_sports,$mat_ninjou,$mat_yuuhuku,$mat_bunka_y,$mat_sports_y,$mat_ninjou_y,$mat_yuuhuku_y,$mat_bunka_z,$mat_sports_z,$mat_ninjou_z,$mat_yuuhuku_z,$mat_yobi1,$mat_yobi2,$mat_yobi3,$mat_yobi4,$mat_yobi5)= split(/<>/);
		$mat_bunka_z = $mat_bunka;
		$mat_sports_z = $mat_sports;
		$mat_ninjou_z = $mat_ninjou;
		$mat_yuuhuku_z = $mat_yuuhuku;
		$mat_bunka_y = 0; $mat_sports_y = 0; $mat_ninjou_y = 0; $mat_yuuhuku_y = 0;
		$mat_bunka = 0; $mat_sports = 0; $mat_ninjou = 0; $mat_yuuhuku = 0;
		$saisyuu_temp = "$mat_num<>$mat_bunka<>$mat_sports<>$mat_ninjou<>$mat_yuuhuku<>$mat_bunka_y<>$mat_sports_y<>$mat_ninjou_y<>$mat_yuuhuku_y<>$mat_bunka_z<>$mat_sports_z<>$mat_ninjou_z<>$mat_yuuhuku_z<>$mat_yobi1<>$mat_yobi2<>$mat_yobi3<>$mat_yobi4<>$mat_yobi5<>\n";
		push (@change_mati_alldata,$saisyuu_temp);
	}
	@mati_alldata = ();
	@mati_alldata = @change_mati_alldata;
	$nannitime_hozon =1;
	$rank_hiduke = "$date2";
	$dainankai_con ++;
	$start_con_time = $date_sec;
	$nannitime_con = 1;		#最初の表示用に１を入れる
	$saisyuu_matikon_settei = "$start_con_time<>$nannitime_hozon<>$dainankai_con<>$rank_hiduke<>\n";
	unshift (@change_mati_alldata,$saisyuu_matikon_settei);
			
#功労者データ更新
	open(KOR,"< $kourousya_logfile") || &error("$kourousya_logfileが開けません");
	eval{ flock (KOR, 1); };
	my @kourou_alldata = <KOR>;
	close(KOR);
	my @new_kourou_alldata = ();
	foreach (@kourou_alldata){
		my ($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
		$kourou_yobi2 = $kourou_total;
		$kourou_bunka_z = $kourou_bunka;
		$kourou_sports_z = $kourou_sports;
		$kourou_ninjou_z = $kourou_ninjou;
		$kourou_yuuhuku_z = $kourou_yuuhuku;
		$kourou_yobi3 += $kourou_total;
		$kourou_total = 0; $kourou_bunka = 0; $kourou_sports = 0; $kourou_ninjou = 0; $kourou_yuuhuku = 0; 
		my $kourou_temp = "$kourou_id<>$kourou_name<>$kourou_total<>$kourou_bunka<>$kourou_sports<>$kourou_ninjou<>$kourou_yuuhuku<>$kourou_bunka_z<>$kourou_sports_z<>$kourou_ninjou_z<>$kourou_yuuhuku_z<>$kourou_yobi1<>$kourou_yobi2<>$kourou_yobi3<>$kourou_yobi4<>$kourou_yobi5<>\n";
		push (@new_kourou_alldata,$kourou_temp);
	}		#foreachの閉じ
			
#データ更新
	open(OUT,">$maticon_logfile") || &error("Open Error : $maticon_logfile");
	eval{ flock (OUT, 2); };
	print OUT @change_mati_alldata;
	close(OUT);
	$saisyuu_flag=1;

	open(KOO,">$kourousya_logfile") || &error("$kourousya_logfileに書き込めません");
	eval{ flock (KOO, 2); };
	print KOO @new_kourou_alldata;
	close(KOO);
	&unlock;
}

#優勝の住人への賞金配布
sub syoukin_haihu {
	&lock;
	$yuusyou_taun = @_[0];
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
		my @ori_ie_para = <IN>;
	close(IN);
#住人の数を計算
	$syoukin_taisyousya = 0;
	foreach (@ori_ie_para){
my ($ori_k_id,$ori_ie_name,$ori_ie_setumei,$ori_ie_image,$ori_ie_syubetu,$ori_ie_kentikubi,$ori_ie_town,$ori_ie_tateziku,$ori_ie_yokoziku,$ori_ie_sentaku_point,$ori_ie_rank,$ori_ie_yobi7,$ori_ie_yobi8,$ori_ie_yobi9,$ori_ie_yobi10)= split(/<>/);
		if ($ori_ie_town eq "$yuusyou_taun" && $ori_k_id !~ /_/){$syoukin_taisyousya ++;} #koko2008/04/01
	}
	if(!$syoukin_taisyousya){return;}
	$syoukingaku = int($mati_con_syoukin*10000/$syoukin_taisyousya);

	foreach (@ori_ie_para){
 ($ori_k_id,$ori_ie_name,$ori_ie_setumei,$ori_ie_image,$ori_ie_syubetu,$ori_ie_kentikubi,$ori_ie_town,$ori_ie_tateziku,$ori_ie_yokoziku,$ori_ie_sentaku_point,$ori_ie_rank,$ori_ie_yobi7,$ori_ie_yobi8,$ori_ie_yobi9,$ori_ie_yobi10)= split(/<>/);
		if ($ori_ie_town eq "$yuusyou_taun" && $ori_k_id !~ /_/){ #koko2008/04/01
			$haihusaki_dir = "./member/$ori_k_id/log.cgi";			#ver.1.40
			if (-e "$haihusaki_dir"){			#ver.1.40
				&openAitelog ($ori_k_id);
				$aite_bank += $syoukingaku;
				&aite_temp_routin;
				open(OUT,">$aite_log_file") || &error("$aite_log_fileに書き込めません");
				eval{ flock (OUT, 2); };
				print OUT $aite_k_temp;
										close(OUT);
				$kityou_naiyou = "街コンテスト賞金($syoukin_taisyousya人)"."@_[1]";
				&aite_kityou_syori("$kityou_naiyou","",$syoukingaku,$aite_bank,"普",$ori_k_id,"lock_off");
			}			#ver.1.40
		}
	}
	&unlock;
}

#優勝の住人への賞金配布２投票者のポイントに応じて分配
sub syoukin_haihu_sanka {
	#投票ポイントの数を計算
	$total_para = 0;
	$sanksya = 0;
	foreach (@kourou_alldata0){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
		if($kourou_yobi4 eq $town_hairetu[$_[0]] && $kourou_yobi4 ne "0"){
			if($_[1] eq "（文化度）"){$total_para += $kourou_bunka_z;}
			if($_[1] eq "（スポーツ振興度）"){$total_para += $kourou_sports_z;}
			if($_[1] eq "（人気度）"){$total_para += $kourou_ninjou_z;}
			if($_[1] eq "（裕福度）"){$total_para += $kourou_yuuhuku_z/10000;}
			$sanksya++;
		}
	}
	if($total_para == 0){return;}
	if($sanksya == 0){return;}
	$syoukingaku_1para = int($mati_con_syoukin*10000/$total_para);
	$sankawari = int($mati_con_syoukin*10000/$sanksya);
#賞金授与
	foreach (@kourou_alldata0){
		($kourou_id,$kourou_name,$kourou_total,$kourou_bunka,$kourou_sports,$kourou_ninjou,$kourou_yuuhuku,$kourou_bunka_z,$kourou_sports_z,$kourou_ninjou_z,$kourou_yuuhuku_z,$kourou_yobi1,$kourou_yobi2,$kourou_yobi3,$kourou_yobi4,$kourou_yobi5)= split(/<>/);
		if($kourou_yobi4 eq $town_hairetu[$_[0]] && $kourou_yobi4 ne "0"){
			$haihusaki_dir = "./member/$kourou_id/log.cgi";			#ver.1.40
			if (-e "$haihusaki_dir"){			#ver.1.40
				if($koroubunpai eq 'yes'){
					if($_[1] eq "（文化度）"){$syoukingaku = $kourou_bunka_z * $syoukingaku_1para;}
					if($_[1] eq "（スポーツ振興度）"){$syoukingaku = $kourou_sports_z * $syoukingaku_1para;}
					if($_[1] eq "（人気度）"){$syoukingaku = $kourou_ninjou_z * $syoukingaku_1para;}
					if($_[1] eq "（裕福度）"){$syoukingaku = ($kourou_yuuhuku_z/10000) * $syoukingaku_1para;}
				}else{$syoukingaku = $sankawari;}
				&openAitelog ($kourou_id);
				if($aite_name ne $kourou_name){next;}
				$aite_bank += $syoukingaku;
				&aite_temp_routin;
				open(OUT,">$aite_log_file") || &error("$aite_log_fileに書き込めません");
				eval{ flock (OUT, 2); };
				print OUT $aite_k_temp;
				close(OUT);
				if($koroubunpai eq 'yes'){
					$kityou_naiyou = "街コンテスト賞金(1ポイント$syoukingaku_1para円)"."$_[1]";
				}else{$kityou_naiyou = "街コンテスト賞金(参加者$sanksya人$sankawari円)"."$_[1]";}
				&aite_kityou_syori("$kityou_naiyou","",$syoukingaku,$aite_bank,"普",$kourou_id);
			}			#ver.1.40
		}
	}
}
