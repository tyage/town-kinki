#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。#2006/10/20 OUT

# 子育ての÷数値 
$kosodatewaruatai = 1;

# カップルランキング表示(yes,no) koko2007/06/22
$kapul_disp = 'yes';

# 子供の性別をランダムに付ける。
$kodomo_seibetu = 'yes';
# eval{ flock (OUT, 2); }; ロック強化 for (0..50){$i=0;}2007/09/02
######################
$this_script = 'kekkon.cgi';
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
	if($in{'mode'} eq "assenjo"){&assenjo;}
	elsif($in{'mode'} eq "kokuhaku"){&kokuhaku;}
	elsif($in{'mode'} eq "renai"){&renai;}
	elsif($in{'mode'} eq "kodomo_naming"){&kodomo_naming;}
	elsif($in{'mode'} eq "kosodate"){&kosodate;}
	elsif($in{'mode'} eq "wakare"){&wakare;}
	elsif($in{'mode'} eq "wakare_do"){&wakare_do;}
	else{&error("「戻る」ボタンで街に戻ってください");}
exit;
	
#############以下サブルーチン
sub assenjo {
#性別のselect
	@as_sex_array=('男','女');
#選択式プロフィール項目
		$as_prof_name1='ただいま';
		@as_prof_array1=('','結婚を前提に恋人募集中','結婚しているが恋人募集中','恋人募集中','結婚しています','恋人が規定数に達しています','今は恋人を募集していません');
		
	open(IN,"< $as_profile_file") || &error("Open Error : $as_profile_file");
	eval{ flock (IN, 1); };
	@alldata=<IN>;
	close(IN);
#カップルランキングの場合
	if ($in{'command'} eq "couple_ranking"){
	open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
	eval{ flock (COA, 1); };
		@all_couple = <COA>;
	close(COA);
	open(REN,"< ./dat_dir/love.cgi") || &error("Open Error : ./dat_dir/love.cgi");
	eval{ flock (REN, 1); };
		$top_koumoku = <REN>;
		my (@koumokumei_hairetu)= split(/<>/,$top_koumoku);
	close(REN);
			&lock;
	$wakareflag = 0;
	$now_time = time ;
	foreach (@all_couple){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
		if ($cn_joutai eq "恋人"){$yobikata = "恋人";$wakare_time = $wakare_limit_koibito;}else{$yobikata = "夫婦";$wakare_time = $wakare_limit_haiguu;}
#別れ処理
		if ($now_time - $cn_yobi1 > $wakare_time * 60 * 60 * 24){
			$wakareflag = 1;

			$cn_yobi1 = 0; #koko2006/06/04

		#	&news_kiroku("別れ","$cn_name1さんと$cn_name2さんが別れました。"); #koko2007/05/28
			if ($yobikata eq "夫婦"){
				&kekkon_id_sakujo($cn_name1);
		#		&kekkon_id_sakujo($cn_name2);
			}
			next;
		}
		push (@new_all_couple_sort,$_);
	}		#foreach閉じ
#データ更新
	if ($wakareflag == 1){
			open(COP,">$couple_file") || &error("$couple_fileに書き込めません");
			eval{ flock (COP, 2); };
			print COP @new_all_couple_sort;
			close(COP);
	}
			&unlock;

#ver.1.40ここから#koko2006/03/11
#	foreach (@new_all_couple_sort){
#			$data=$_;


#			$key=(split(/<>/,$data))[4];		#ソートする要素を選ぶ
#			$key1=(split(/<>/,$data))[5];		#ソートする要素を選ぶ
#			$key2=(split(/<>/,$data))[6];		#ソートする要素を選ぶ
#			$key3=(split(/<>/,$data))[7];		#ソートする要素を選ぶ
#			$key4=(split(/<>/,$data))[8];		#ソートする要素を選ぶ
#			$key5=(split(/<>/,$data))[9];		#ソートする要素を選ぶ
#			push @all_couple_sort,$data;

#			push @keys,$key;
#			push @keys1,$key1;
#			push @keys2,$key2;
#			push @keys3,$key3;
#			push @keys4,$key4;
#			push @keys5,$key5;
#	}


#		sub bykeys{$keys[$b] <=> $keys[$a];}
#		sub bykeys1{$keys1[$b] <=> $keys1[$a];}
#		sub bykeys2{$keys2[$b] <=> $keys2[$a];}
#		sub bykeys3{$keys3[$b] <=> $keys3[$a];}
#		sub bykeys4{$keys4[$b] <=> $keys4[$a];}
#		sub bykeys5{$keys5[$b] <=> $keys5[$a];}
#		@all_couple_sort0=@all_couple_sort[ sort bykeys 0..$#all_couple_sort];
#		@all_couple_sort1=@all_couple_sort[ sort bykeys1 0..$#all_couple_sort];
#		@all_couple_sort2=@all_couple_sort[ sort bykeys2 0..$#all_couple_sort];
#		@all_couple_sort3=@all_couple_sort[ sort bykeys3 0..$#all_couple_sort];
#		@all_couple_sort4=@all_couple_sort[ sort bykeys4 0..$#all_couple_sort];
#		@all_couple_sort5=@all_couple_sort[ sort bykeys5 0..$#all_couple_sort];
		@all_couple_sort = @new_all_couple_sort;
		@keys0 = map {(split /<>/)[4]} @all_couple_sort;
		@all_couple_sort0 = @all_couple_sort[sort {$keys0[$b] <=> $keys0[$a]} 0 .. $#keys0];

		@keys1 = map {(split /<>/)[5]} @all_couple_sort;
		@all_couple_sort1 = @all_couple_sort[sort {$keys1[$b] <=> $keys1[$a]} 0 .. $#keys1];

		@keys2 = map {(split /<>/)[6]} @all_couple_sort;
		@all_couple_sort2 = @all_couple_sort[sort {$keys2[$b] <=> $keys2[$a]} 0 .. $#keys2];

		@keys3 = map {(split /<>/)[7]} @all_couple_sort;
		@all_couple_sort3 = @all_couple_sort[sort {$keys3[$b] <=> $keys3[$a]} 0 .. $#keys3];

		@keys4 = map {(split /<>/)[8]} @all_couple_sort;
		@all_couple_sort4 = @all_couple_sort[sort {$keys4[$b] <=> $keys4[$a]} 0 .. $#keys4];

		@keys5 = map {(split /<>/)[9]} @all_couple_sort;
		@all_couple_sort5 = @all_couple_sort[sort {$keys5[$b] <=> $keys5[$a]} 0 .. $#keys5];
#kokoend2006/03/12

		&header(assen_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>現在成立している全てのカップルです。<br>ラブラブ度の多い順に並んでいます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">ラブラブ&hearts;カップルランキング</div>
	</td></tr></table><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
EOM

		print "<tr  class=jouge bgcolor=#ffffcc><td style=\"color:#3366ff\">「$koumokumei_hairetu[2]」の多いカップル</td>";
		foreach $juni (1..3){
			$sort_no=$koumoku_sentaku-1;
			$one_couple = (split(/<>/,$all_couple_sort1[$juni - 1]))[1];
			$two_couple = (split(/<>/,$all_couple_sort1[$juni - 1]))[2];
			$suuti =  (split(/<>/,$all_couple_sort1[$juni - 1]))[5];
			print "<td><span style=\"color:#3366ff\">NO.$juni</span>：$one_couple & $two_couple（$suuti）</td>";
		}
		print "</tr>";

		print "<tr  class=jouge bgcolor=#ffffff><td style=\"color:#3366ff\">「$koumokumei_hairetu[3]」の多いカップル</td>";
		foreach $juni (1..3){
			$sort_no=$koumoku_sentaku-1;
			$one_couple = (split(/<>/,$all_couple_sort2[$juni - 1]))[1];
			$two_couple = (split(/<>/,$all_couple_sort2[$juni - 1]))[2];
			$suuti =  (split(/<>/,$all_couple_sort2[$juni - 1]))[6];
			print "<td><span style=\"color:#3366ff\">NO.$juni</span>：$one_couple & $two_couple（$suuti）</td>";
		}
		print "</tr>";
		
		print "<tr  class=jouge bgcolor=#ffffcc><td style=\"color:#3366ff\">「$koumokumei_hairetu[4]」の多いカップル</td>";
		foreach $juni (1..3){
			$sort_no=$koumoku_sentaku-1;
			$one_couple = (split(/<>/,$all_couple_sort3[$juni - 1]))[1];
			$two_couple = (split(/<>/,$all_couple_sort3[$juni - 1]))[2];
			$suuti =  (split(/<>/,$all_couple_sort3[$juni - 1]))[7];
			print "<td><span style=\"color:#3366ff\">NO.$juni</span>：$one_couple & $two_couple（$suuti）</td>";
		}
		print "</tr>";
		
		print "<tr  class=jouge bgcolor=#ffffff><td style=\"color:#3366ff\">「$koumokumei_hairetu[5]」の多いカップル</td>";
		foreach $juni (1..3){
			$sort_no=$koumoku_sentaku-1;
			$one_couple = (split(/<>/,$all_couple_sort4[$juni - 1]))[1];
			$two_couple = (split(/<>/,$all_couple_sort4[$juni - 1]))[2];
			$suuti =  (split(/<>/,$all_couple_sort4[$juni - 1]))[8];
			print "<td><span style=\"color:#3366ff\">NO.$juni</span>：$one_couple & $two_couple（$suuti）</td>";
		}
		print "</tr>";
		
		print "<tr  class=jouge bgcolor=#ffffcc><td style=\"color:#3366ff\">「$koumokumei_hairetu[6]」の多いカップル</td>";
		foreach $juni (1..3){
			$sort_no=$koumoku_sentaku-1;
			$one_couple = (split(/<>/,$all_couple_sort5[$juni - 1]))[1];
			$two_couple = (split(/<>/,$all_couple_sort5[$juni - 1]))[2];
			$suuti =  (split(/<>/,$all_couple_sort5[$juni - 1]))[9];
			print "<td><span style=\"color:#3366ff\">NO.$juni</span>：$one_couple & $two_couple（$suuti）</td>";
		}
		print "</tr>";
		
	print <<"EOM";
	</table><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>名前</td><td>関係</td><td>ラブラブ度</td><td>$koumokumei_hairetu[2]</td><td>$koumokumei_hairetu[3]</td><td>$koumokumei_hairetu[4]</td><td>$koumokumei_hairetu[5]</td><td>$koumokumei_hairetu[6]</td></tr>
EOM
	foreach (@all_couple_sort0){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai)= split(/<>/);
		if ($cn_joutai eq "配偶者"){
			$huuhu{"$cn_name1"} = "on";
			$huuhu{"$cn_name2"} = "on";
		}
	}
	
	$i = 1;
	foreach (@all_couple_sort0){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
		if ($cn_joutai eq "恋人"){
			if ($huuhu{"$cn_name1"} eq "on" || $huuhu{"$cn_name2"} eq "on"){
				$yobikata = "愛人";
				$c_color= "#6699cc";
			}else{
				$yobikata = "恋人";
				$c_color= "#ff6600";
			}
		}else{$yobikata = "夫婦";$c_color= "#ff0000";}
		print <<"EOM";
	<tr align=right><td align=center>$i</td><td  align=left style="color:$c_color;">$cn_name1 &hearts; $cn_name2</td><td align=center style="color:$c_color;">$yobikata</td><td class=mainasu>$cn_total_aijou</td><td>$cn_omoide1</td><td>$cn_omoide2</td><td>$cn_omoide3</td><td>$cn_omoide4</td><td>$cn_omoide5</td></tr>
EOM
		$i ++;
	}		#foreach閉じ
#ver.1.40ここまで
	print "</table>";

	&hooter("assenjo","戻る","kekkon.cgi");
	&hooter("login_view","街へ戻る");
	exit;
	}		#カップルランキングの場合閉じ
	
#子供ランキングの場合
	if ($in{'command'} eq "kodomo_ranking"){
	open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
	eval{ flock (KOD, 1); };
	@all_kodomo=<KOD>;
	close(KOD);
		
	$now_time = time ;
	$kodomo_sakujo_flg = 0;
	foreach (@all_kodomo){
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
		chomp $kod_renraku1;
		$kono_nenrei = int (($now_time - $kod_yobi1) / (60*60*24));

#子供削除処理
		if ($kono_nenrei > $kodomo_sibou_time2){
			$kodomo_sakujo_flg = 1;
			next;
		}
		
#子供流産処理
		if ($kod_name eq "" && $now_time - $kod_yobi1 > $kodomo_sibou_time * 60 * 60 * 24 && $kod_yobi8 != 1){
			&lock;
			$kodomo_sakujo_flg = 1;
			&unlock;
			next;
		}
		
#子供死亡処理
		if ($now_time - $kod_yobi7 > $kodomo_sibou_time * 60 * 60 * 24 && $kod_yobi8 != 1){
			&lock;
			$kodomo_sakujo_flg = 1;
			&unlock;
			next;
		}
#子供自立処理
		if ($kono_nenrei >= 19 && $kod_yobi8 != 1){
			&kodomo_ziritu($_);
			$kod_job = $return_job;
			$kod_yobi8 = 1;
			$kodomo_sakujo_flg = 1;
		}
		$new_kodomo_temp = "$kod_num<>$kod_name<>$kod_oya1<>$kod_oya2<>$kod_job<>$kod_kokugo<>$kod_suugaku<>$kod_rika<>$kod_syakai<>$kod_eigo<>$kod_ongaku<>$kod_bijutu<>$kod_looks<>$kod_tairyoku<>$kod_kenkou<>$kod_speed<>$kod_power<>$kod_wanryoku<>$kod_kyakuryoku<>$kod_love<>$kod_unique<>$kod_etti<>$kod_yobi1<>$kod_yobi2<>$kod_yobi3<>$kod_yobi4<>$kod_yobi5<>$kod_yobi6<>$kod_yobi7<>$kod_yobi8<>$kod_yobi9<>$kod_yobi10<>$kod_renraku1<>$kod_renraku2<>\n";
		push @new_all_kodomo,$new_kodomo_temp;

	}		#foreach閉じ
		
#子供データ更新
	if ($kodomo_sakujo_flg == 1){
		&lock;
		open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
		eval{ flock (KODO, 2); };
		print KODO @new_all_kodomo;
		close(KODO);
		&unlock;
	}
#koko2006/03/12
#	foreach (@new_all_kodomo){
#			$data=$_;
#			$key=(split(/<>/,$data))[25];		#ソートする要素を選ぶ
#			push @all_kodomo_sort,$data;
#			push @keys,$key;
#	}
#ソート処理
#		sub bykeys{$keys[$b] <=> $keys[$a];}
#		@all_kodomo_sort=@all_kodomo_sort[ sort bykeys 0..$#all_kodomo_sort];
	@all_kodomo_sort = @new_all_kodomo;
	#	@keys0 = map {(split /<>/)[25]} @all_kodomo_sort;#koko2006/12/09
	@keys0 = map {(split /<>/)[22]} @all_kodomo_sort;#年齢でソート
	@all_kodomo_sort = @all_kodomo_sort[sort {@keys0[$b] <=> @keys0[$a]} 0 .. $#keys0];		
#kokoend2006/03/12
		
	foreach (@all_kodomo_sort){
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
		chomp $kod_renraku1;
		$kono_nenrei = int (($now_time - $kod_yobi1) / (60*60*24));
			
		$kod_yobi5 = sprintf ("%.1f",$kod_yobi5);
		$kod_yobi6 = sprintf ("%.1f",$kod_yobi6);
#koko2007/11/25
		if($kod_yobi10 eq "m"){$sex_color="#0000ff";}
		elsif($kod_yobi10 eq "f"){$sex_color="#ff0000";}
		else{$sex_color="#000000";}
#kokoend
		$ko_meisai_td = "<td><font color=$sex_color>$kod_name</font></td><td>$kod_oya1 &hearts; $kod_oya2</td><td align=right>$kono_nenrei歳</td><td align=right>$kod_yobi5 cm</td><td align=right>$kod_yobi6 kg</td><td align=right>$kod_yobi4</td>";

		$ko_meisai_td2="<td>$kod_name</td><td>$kod_oya1 &hearts; $kod_oya2</td><td align=right>$kono_nenrei歳</td><td align=right>$kod_yobi5 cm</td><td align=right>$kod_yobi6 kg</td><td align=right>$kod_job</td>";
		
		if ($kod_name eq ""){next;}

		if ($kono_nenrei > int(($kodomo_sibou_time2 - 18) / 2)+19){push (@seijin2_hairetu,$ko_meisai_td2);}
		elsif ($kono_nenrei >18){push (@seijin1_hairetu,$ko_meisai_td2);}
		elsif ($kono_nenrei >=16){push (@koukou_hairetu,$ko_meisai_td);}
		elsif ($kono_nenrei >=13){push (@tyuugaku_hairetu,$ko_meisai_td);}
		elsif ($kono_nenrei >=7){push (@syougaku_hairetu,$ko_meisai_td);}
		else{push (@youzi_hairetu,$ko_meisai_td);}
	}
		
		&header(assen_style);
		print <<"EOM";
	<table width="95%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>子供の能\力ランキングです。年齢によって「幼児部門」「小学生部門」「中学生部門」「高校生部門」に分かれます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">子供ランキングベスト20</div>
	</td></tr></table><br>
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr><td valign=top width=50%>
	<div class=tyuu align=center>幼児部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>能\力値</td></tr>
EOM
	$i = 1;
	foreach (@youzi_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
			if ($i >= 20){last;}
	}
	print <<"EOM";
	</table></td><td valign=top width=50%>
	<div class=tyuu align=center>小学生部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>能\力値</td></tr>
EOM
	$i = 1;
	foreach (@syougaku_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
			if ($i >= 20){last;}
	}
	print <<"EOM";
	</table></td></tr></table><br><br>
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr><td valign=top width=50%>
	<div class=tyuu align=center>中学生部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>能\力値</td></tr>
EOM
	$i = 1;
	foreach (@tyuugaku_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
			if ($i >= 20){last;}
	}
	print <<"EOM";
	</table></td><td valign=top width=50%>
	<div class=tyuu align=center>高校生部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>能\力値</td></tr>
EOM
	$i = 1;
	foreach (@koukou_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
			if ($i >= 20){last;}
	}
#koko2006/12/09
	print <<"EOM";
	</table></td></tr></table><br><br>
	<table width="95%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr><td valign=top width=50%>
	<div class=tyuu align=center>成人部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>職業</td></tr>
EOM
	$i = 1;
	foreach (@seijin1_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
		#	if ($i >= 20){last;}
	}
	print <<"EOM";
	</table></td><td valign=top width=50%>
	<div class=tyuu align=center>老齢部門</div>
	<table width="100%" border="0" cellspacing="0" cellpadding="5" align=center class=yosumi>
	<tr  class=jouge bgcolor=#ffffaa align=center nowrap><td>順位</td><td>子供の名前</td><td>親の名前</td><td>年齢</td><td>身長</td><td>体重</td><td>職業</td></tr>
EOM
	$i = 1;
	foreach (@seijin2_hairetu){
			print "<tr><td align=center>$i</td>$_</tr>";
			$i ++;
		#	if ($i >= 20){last;}
	}
#kokoend
	print "</table></td></tr></table>";

	print "<br><div align=center><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>";
	&hooter("login_view","街へ戻る");
	exit;
	}		#子供ランキングの場合閉じ
	
#プロフィール削除の場合
	if ($in{'command'} eq "touroku_sakujo"){
	&lock;
#ver.1.40ここから
	open(ASP,"< $as_profile_file") || &error("Open Error : $as_profile_file");
	eval{ flock (ASP, 1); };
	my @as_pro_alldata=<ASP>;
	close(ASP);
	@as_new_pro_alldata = ();
	foreach (@as_pro_alldata){
my ($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			if ($in{'name'} eq "$pro_name"){next;} 
			push (@as_new_pro_alldata,$_);
	}
#ログ更新
	open(ASPO,">$as_profile_file") || &error("$as_profile_fileに書き込めません");
	eval{ flock (ASPO, 2); };
	print ASPO @as_new_pro_alldata;
	close(ASPO);
#		&as_prof_sakujo($in{'name'});
#ver.1.40ここまで
	&unlock;
	&message_only("恋人斡旋所のプロフィールを削除しました。");
	&hooter("assenjo","戻る","kekkon.cgi");
	exit;
	}
	
#登録フォームの出力
	if ($in{'command'} eq "touroku_form"){
		&as_prof_form;
		exit;
	}
	
#登録の場合
	if ($in{'command'} eq "touroku"){
		if ($love < $need_love){&error("登録するのに必要なLOVEパラメータが足りません");}
		$atta_flag=0;
		@new_alldata = ();
		foreach (@alldata){
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
#修正の場合
			if ($name eq "$pro_name"){next;} 
			push (@new_alldata,$_);
		}
		my($new_entry) = "$name<>$in{'pro_sex'}<>$in{'pro_age'}<>$in{'pro_addr'}<>$in{'pro_p1'}<>$in{'pro_p2'}<>$in{'pro_p3'}<>$in{'pro_p4'}<>$in{'pro_p5'}<>$in{'pro_p6'}<>$in{'pro_p7'}<>$k_sousisan<>$k_id<>$job<>$in{'pro_p11'}<>$in{'pro_p12'}<>$in{'pro_p13'}<>$in{'pro_p14'}<>$in{'pro_p15'}<>$in{'pro_p16'}<>$in{'pro_p17'}<>$in{'pro_p18'}<>$in{'pro_p19'}<>$in{'pro_p20'}<>\n";
#pro_p7までがプロフィール　pro_p8＝総資産　pro_p9＝ID番号（家表示用）pro_p10＝職業
		unshift (@new_alldata,$new_entry);
		
#ログ更新
	&lock;
	open(OUT,">$as_profile_file") || &error("$profile_fileに書き込めません");
	eval{ flock (OUT, 2); };
	print OUT @new_alldata;
	close(OUT);
	&unlock;
	&message("恋人斡旋所のプロフィール登録を行いました。","assenjo","kekkon.cgi");
	exit;
	}
	if ($love < $need_love){$keikoku = "※LOVEパラメータが足らないため、$nameさんはまだ登録できません。";}
	&header(assen_style);
		print <<"EOM";
	<table width="95%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●ここに登録することでバーチャルな恋愛や結婚をすることができるようになります。<br>
	●登録するにはLOVEパラメータが$need_love以上必要です（パラメータウインドウの上部には新たにハートマークのアイコンが現れます）。<br>
	●登録が済んだ方は、こちらで好きな方に交際の申\し込みをしたり、交際申\し込みメールを受け取ったりできるようになります。<br>
	●配偶者、恋人を合わせ、同時に$koibito_seigen人の方とおつき合いができます。<br>
	●恋人ができると、ハートマークのアイコンから恋愛コマンドが使えるようになります。<br>
	●結婚するためには、恋愛コマンドによって恋人になった方とのラブラブ度を深めていく必要があります。<br>
	<font color=#336699>$keikoku</font>
	</td>
	<td bgcolor="#ffff99" align=center width="300"><font color="#ff0000" size="5"><b>恋人斡旋所</b></font></td>
	</td></tr></table><br>

	<table width="95%" border="0" cellspacing="0" cellpadding="8" align=center bgcolor=#ffffff>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="easySerch">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<tr>
EOM

#検索フォーム
# 名前
	print "<td>名　前 <input type=text name=serch_name size=20></td>\n";

# 年齢
	print "<td><select name=age>\n";
	print "<option value=\"\">年齢\n";
		for($i=1;$i<@as_age_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'age'} eq $as_age_array[$i]);
				print ($option,$as_age_array[$i]);
		}
	print "</select></td>\n";
	
# 住所
	print "<td><select name=address>\n";
	print "<option value=\"\">住所\n";
		for($i=1;$i<@as_address_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'address'} eq $as_address_array[$i]);
				print ($option,$as_address_array[$i]);
		}
	print "</select></td>\n";
	
# プロフ1
	print "<td valign=top nowrap>\n";
	print "<select name=p1>\n";
	print "<option value=\"\">$as_prof_name1\n";
		for($i=1;$i<@as_prof_array1;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p1'} eq $as_prof_array1[$i]);
				print ($option,$as_prof_array1[$i]);
		}
	print "</select></td>\n";
	
# プロフ2
	print "<td valign=top nowrap>\n";
	print "<select name=p2>\n";
	print "<option value=\"\">$as_prof_name2\n";
		for($i=1;$i<@as_prof_array2;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p2'} eq $as_prof_array2[$i]);
				print ($option,$as_prof_array2[$i]);
		}
	print "</select></td></tr><tr>\n";
	
# プロフ3
	print "<td valign=top nowrap>\n";
	print "<select name=p3>\n";
	print "<option value=\"\" selected>$as_prof_name3\n";
		for($i=1;$i<@as_prof_array3;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p3'} eq $as_prof_array3[$i]);
				print ($option,$as_prof_array3[$i]);
		}
	print "</select></td>\n";
	
# プロフ4
	print "<td valign=top nowrap>\n";
	print "<select name=p4>\n";
	print "<option value=\"\" selected>$as_prof_name4\n";
		for($i=1;$i<@as_prof_array4;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p4'} eq $as_prof_array4[$i]);
				print ($option,$as_prof_array4[$i]);
		}
	print "</select></td>\n";
	
# プロフ5
	print "<td valign=top nowrap>\n";
	print "<select name=p5>\n";
	print "<option value=\"\" selected>$as_prof_name5\n";
		for($i=1;$i<@as_prof_array5;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p5'} eq $as_prof_array5[$i]);
				print ($option,$as_prof_array5[$i]);
		}
	print "</select></td>\n";
	
# プロフ6
	print "<td valign=top nowrap>\n";
	print "<select name=p6>\n";
	print "<option value=\"\" selected>$as_prof_name6\n";
		for($i=1;$i<@as_prof_array6;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p6'} eq $as_prof_array6[$i]);
				print ($option,$as_prof_array6[$i]);
		}

	print <<"EOM";
	</select></td><td>
	<input type=submit value=" 検索する ">
	</form>
	  </td>
    </tr>
  </table><br>
	<table border=0 align=center width=400>
	<tr><td align=left>
EOM
#koko2007/06/22
	if ($kapul_disp eq 'yes'){
		print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="couple_ranking">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="カップルランキング">
	</form>
EOM
	}
	print <<"EOM";
	</td><td align=right>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="kodomo_ranking">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="子供ランキング">
	</form>
	</td></tr></table><br>
EOM
		
	$page=$in{'page'};	
	if ($page eq "") { $page = 0; }
	$i3=0;

##ログ表示処理
#個人の家情報をunitハッシュに代入
	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (OI, 1); };
	@ori_ie_hairetu = <OI>;
	foreach (@ori_ie_hairetu) {
		&ori_ie_sprit($_);
		$unit{"$ori_k_id"} = "<img src=\"$ori_ie_image\">";
	}
	close(OI);
	
#自分のプロフィールを表示
	foreach (@alldata) {
		($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
		@my_prof_hairetu = split(/<>/);
		if ($name eq "$pro_name"){
			$prof_atta_flg = 1;
            last;
        }
	}

if ($in{'command'} ne "easySerch"){		#検索の場合は自分のプロフィールを表示しない
			if($pro_sex eq "男"){
					$sex_style="border: #ffffff; border-style: solid; border-width: 2px; background-color:#ffffff";
			}elsif($pro_sex eq "女"){
					$sex_style="border: #ffffff; border-style: solid; border-width: 2px; background-color:#ffffff";
			}
			if ($unit{"$pro_p9"} ne ""){$ie_hyouzi="$unit{$pro_p9}"}else{$ie_hyouzi="：無し";}
			if ($prof_atta_flg == 0){$zibun_prof_com = "<tr><td align=center colspan=8>登録していません。</td></tr>";}else{
				$zibun_prof_com =<< "EOM";
<tr>
<td width=25%><span class=honbun2>名前</span>：$pro_name（$pro_p10）</td>
<td width=25%><span class=honbun2>性別</span>：$pro_sex</td>
<td width=25%><span class=honbun2>総資産</span>：$pro_p8円</td>
<td width=25%><span class=honbun2>家</span>$ie_hyouzi</td>
</tr>
<tr>
<td width=25%><span class=honbun2>年齢</span>：$pro_age</td>
<td width=25%><span class=honbun2>住所</span>：$pro_addr</td>
<td width=25%><span class=honbun2>$as_prof_name1</span>：$pro_p1</td>
<td width=25%><span class=honbun2>$as_prof_name2</span>：$pro_p2</td>
</tr>
<tr>
<td width=25%><span class=honbun2>$as_prof_name3</span>：$pro_p3</td>
<td width=25%><span class=honbun2>$as_prof_name4</span>：$pro_p4</td>
<td width=25%><span class=honbun2>$as_prof_name5</span>：$pro_p5</td>
<td width=25%><span class=honbun2>$as_prof_name6</span>：$pro_p6</td>
</tr>
<tr>
<td colspan=8>
<span class=honbun2>一言コメント</span>：$pro_p7<br><br>
※職業、総資産、家などこちらで更新しないと最新の情報になりません。<br>
※結婚したり、すでに規定の恋人数に達している方は「ただいま」の項目を随意変更してください。
</td>
</tr>

EOM
			}
			print <<"EOM";
<table style=\"$sex_style\" align=center width=95%>
<tr><td colspan=8 align=center><span class=honbun2><b>＜自分のプロフィール＞</b></td></tr>
$zibun_prof_com
<tr><td width=120 colspan=8 align=center>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="assenjo">
<input type=hidden name=command value="touroku_form">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="プロフィール登録＆修正">
</form>
</td></tr>
</table><br>
<br>
EOM
}

	
# 簡易検索の場合
		if ($in{'command'} eq "easySerch"){
				$i=0;
				foreach (@alldata) {
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
					if ($in{'serch_name'} ne "" && $in{'serch_name'} ne $pro_name) { next; }		#条件が一致しなかった時点で次の人へ
					if ($in{'age'} ne "" && $in{'age'} ne $pro_age) { next; }		
					if ($in{'address'} ne "" && $in{'address'} ne $pro_addr) { next; }
					if ($in{'p1'} ne "" && $in{'p1'} ne $pro_p1) { next; }
					if ($in{'p2'} ne "" && $in{'p2'} ne $pro_p2) { next; }
					if ($in{'p3'} ne "" && $in{'p3'} ne $pro_p3) { next; }
					if ($in{'p4'} ne "" && $in{'p4'} ne $pro_p4) { next; }
					if ($in{'p5'} ne "" && $in{'p5'} ne $pro_p5) { next; }
					if ($in{'p6'} ne "" && $in{'p6'} ne $pro_p6) { next; }
			if ($name eq "$pro_name"){next;}
			if ($douseiai_per == 0){
				if ($sex eq "m" && $pro_sex eq "男"){next;}
				if ($sex eq "f" && $pro_sex eq "女"){next;}
			}
					$i++;
					push(@newrank,$_);
				}
				@alldata=@newrank;
				print "<div align=center class=sub2>条件にヒットしたのは$i件です。<br>
				<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
				</div><br>";
				&hooter("assenjo","全て表\示","kekkon.cgi");
		}
#全員のプロフィールを表示
			if ($douseiai_per == 0){
				if ($sex eq "m"){$tourokusya_hyouki = "＜現在の女性登録者＞";}
				elsif ($sex eq "f"){$tourokusya_hyouki = "＜現在の男性登録者＞";}
			}else{$tourokusya_hyouki = "＜現在の登録者＞";}
	print <<"EOM";
	<div align=center class="honbun4">$tourokusya_hyouki</div><br>
EOM

#持ち物リストからギフト配列作成koko2007/12/20
	if(!$k_id){&error("mono.cgi エラー command6")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$gift_select ="";
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "ギフト"){
			$gift_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
	}
#kokoend
		foreach (@alldata) {
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			@my_prof_hairetu = split(/<>/);
			if ($name eq "$pro_name"){next;}
			if ($douseiai_per == 0){
				if ($sex eq "m" && $pro_sex eq "男"){next;}
				if ($sex eq "f" && $pro_sex eq "女"){next;}
			}
		$i3++;
		if ($i3 < $page + 1) { next; }
		if ($i3 > $page + $hyouzi_max_grobal) { last; }
		
			if($pro_sex eq "男"){
					$sex_style="border: #ffff99; border-style: double; border-width: 7px; background-color:#ffff99";
			}elsif($pro_sex eq "女"){
					$sex_style="border: #ffff99; border-style: double; border-width: 7px; background-color:#ffff99";
			}
			if ($unit{"$pro_p9"} ne ""){$ie_hyouzi="$unit{$pro_p9}"}else{$ie_hyouzi="：無し";}
#総資産のコンマ処理
			if ($pro_p8 =~ /^[-+]?\d\d\d\d+/g) {
			  for ($i = pos($pro_p8) - 3, $j = $pro_p8 =~ /^[-+]/; $i > $j; $i -= 3) {
			    substr($pro_p8, $i, 0) = ',';
			  }
			}
			print <<"EOM";
			<table style=\"$sex_style\" align=center width=450>
			<tr><td align=right width=120><div class=honbun2>名前</div></td><td>：$pro_name（$pro_p10）</td></tr>
			<tr><td align=right width=120><div class=honbun2>性別</div></td><td>：$pro_sex</td></tr>
			<tr><td align=right width=120><div class=honbun2>総資産</div></td><td>：$pro_p8円</td></tr>
			<tr><td align=right width=120><div class=honbun2>家</div></td><td>$ie_hyouzi</td></tr>
EOM
			$i=0;
			foreach (@my_prof_hairetu){
					$_ =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
					$i ++; 
					if ($i <= 2){next;}
					if ($i >= 12){last;}
					elsif ($i == 3){$pr_koumokumei ="年齢";}
					elsif ($i == 4){$pr_koumokumei ="住所";}
					elsif ($i == 5){$pr_koumokumei ="$as_prof_name1";}
					elsif ($i == 6){$pr_koumokumei ="$as_prof_name2";}
					elsif ($i == 7){$pr_koumokumei ="$as_prof_name3";}
					elsif ($i == 8){$pr_koumokumei ="$as_prof_name4";}
					elsif ($i == 9){$pr_koumokumei ="$as_prof_name5";}
					elsif ($i == 10){$pr_koumokumei ="$as_prof_name6";}
					elsif ($i == 11) {$pr_koumokumei = "一言コメント";}
				if ($_ ne "" && $_ ne "\n"){
					print <<"EOM";
					<tr><td align=right width=120><div class=honbun2>$pr_koumokumei</div></td>
					<td>：$_</td></tr>
EOM
				}
		}	#foreach閉じ
#LOVEパラメータが超えて登録が済んでいたらフォーム出力
		if ($love >= $need_love && $prof_atta_flg == 1){


			print <<"EOM";
     <tr><td colspan=2 align=center>
	 <form method="POST" action="$this_script">
	<input type=hidden name=mode value="kokuhaku">
	<input type=hidden name=kokuhaku_syubetu value="mousikomi">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name="sousinsaki_name" value="$pro_name">
	告白の言葉 <textarea rows=2 name=m_com cols=50 ></textarea>
	<input type=submit value="交際を申\し込む"><br>
	●プレゼント送付<!-- koko2007/12/20 -->
	<select name=gift_souhu>
	<option value="">無し</option>
	$gift_select
	</select><br>	
</form>
EOM
#kokoend
		}
		print <<"EOM";
	</td></tr>
	</table><br>
EOM

		}	#foreachの閉じ（ログ表示処理ここまで）

		$next = $page + $hyouzi_max_grobal;
		$back = $page - $hyouzi_max_grobal;
		print "<div align=center><table border=0><tr>";
		if ($back >= 0) {
#検索の場合のボタン
				if($in{'command'} eq "easySerch"){
					print <<"EOM";
			<form method=POST action="$this_script">
			<input type=hidden name=mode value="assenjo">
			<input type=hidden name=command value="easySerch">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=sex value="$in{'sex'}">
			<input type=hidden name=age value="$in{'age'}">
			<input type=hidden name=address value="$in{'address'}">
			<input type=hidden name=p1 value="$in{'p1'}">
			<input type=hidden name=p2 value="$in{'p2'}">
			<input type=hidden name=p3 value="$in{'p3'}">
			<input type=hidden name=p4 value="$in{'p4'}">
			<input type=hidden name=p5 value="$in{'p5'}">
			<input type=hidden name=p5 value="$in{'p6'}">
			<input type=hidden name=page value="$back">
			<input type=submit value="BACK">
			</form>
EOM
				}else{
#通常の場合
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="assenjo">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=page value="$back">
			<input type=submit value="BACK"></form></td>
EOM
				}
		}
		if ($next < $i3) {
				if($in{'command'} eq "easySerch"){
					print <<"EOM";
			<form method=POST action="$this_script">
			<input type=hidden name=mode value="assenjo">
			<input type=hidden name=command value="easySerch">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=sex value="$in{'sex'}">
			<input type=hidden name=age value="$in{'age'}">
			<input type=hidden name=address value="$in{'address'}">
			<input type=hidden name=p1 value="$in{'p1'}">
			<input type=hidden name=p2 value="$in{'p2'}">
			<input type=hidden name=p3 value="$in{'p3'}">
			<input type=hidden name=p4 value="$in{'p4'}">
			<input type=hidden name=p5 value="$in{'p5'}">
			<input type=hidden name=p6 value="$in{'p6'}">
			<input type=hidden name=page value="$next">
			<input type=submit value="NEXT">
</form>
EOM
				}else{
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="assenjo">
			<input type=hidden name=name value="$in{'name'}">
			<input type=hidden name=pass value="$in{'pass'}">
			<input type=hidden name=town_no value="$in{'town_no'}">
			<input type=hidden name=page value="$next">
			<input type=submit value="NEXT"></form></td>
EOM
				}
		}
		print "</tr></table>";

	&hooter("login_view","街へ戻る");
	exit;
}

##登録フォーム
sub as_prof_form {
		if ($love < $need_love){&error("登録するのに必要なLOVEパラメータが足りません");}
		$atta_flag = 0;
		foreach (@alldata){
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			@my_prof_hairetu = split(/<>/);
			if ($pro_name eq "$name"){$atta_flag = 1; last;}
		}
	if ($atta_flag == 0){
	$pro_name = ""; $pro_sex = ""; $pro_age = ""; $pro_addr = ""; $pro_p1 = ""; $pro_p2 = ""; $pro_p3 = ""; $pro_p4 = ""; $pro_p5 = ""; $pro_p6 = ""; $pro_p7 = ""; $pro_p8 = ""; $pro_p9 = ""; $pro_p10 = ""; $pro_p11 = ""; $pro_p12 = ""; $pro_p13 = ""; $pro_p14 = ""; $pro_p15 = ""; $pro_p16 = ""; $pro_p17 = ""; $pro_p18 = ""; $pro_p19 = ""; $pro_p20 = "";
	@my_prof_hairetu = ();
	}
	
	&header(assen_style);
	if ($sex eq "m"){$sex_sentaku = "男"}else{$sex_sentaku = "女"}
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="touroku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=pro_sex value="$sex_sentaku">
	<input type=hidden name=town_no value="$in{'town_no'}">
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●公開したい項目のみ選択または記述し、その他は空白のままでOKです。<br>
	●「ただいま」の項目はゲーム内での状態を選択してください。結婚したり、すでに規定の恋人数に達している方は随意変更するようにしてください。<br>
	●修正・更新はいつでもできます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">恋人斡旋所プロフィール登録</div>
	</td></tr></table><br>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
EOM
		print ' 年齢<br><select name="pro_age">';
		for($i=0;$i<@as_age_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($pro_age eq $as_age_array[$i]);
				print ($option,$as_age_array[$i]);
		}
		print '</select></td><td>';


		print ' 住所<br><select name="pro_addr">';
		for($i=0;$i<@as_address_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($pro_addr eq $as_address_array[$i]);
				print ($option,$as_address_array[$i]);
		}
		print '</select></td><td>';

 		print "$as_prof_name1<br><select name=\"pro_p1\">";
		for($i=0;$i<@as_prof_array1;$i++){
				$option='<option>';
				$option='<option selected>' if($pro_p1 eq $as_prof_array1[$i]);
				print ($option,$as_prof_array1[$i]);
		}
		print '</select></td><td>';

		print "$as_prof_name2<br><select name=\"pro_p2\">";
		for($i=0;$i<@as_prof_array2;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p2 eq $as_prof_array2[$i]);
				print ($option,$as_prof_array2[$i]);
		}
		print '</select></td></tr><tr><td>';
 
 		print "$as_prof_name3<br><select name=\"pro_p3\">";
		for($i=0;$i<@as_prof_array3;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p3 eq $as_prof_array3[$i]);
				print ($option,$as_prof_array3[$i]);
		}
		print '</select></td><td>';
 
 		print "$as_prof_name4<br><select name=\"pro_p4\">";
		for($i=0;$i<@as_prof_array4;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p4 eq $as_prof_array4[$i]);
				print ($option,$as_prof_array4[$i]);
		}
		print '</select></td><td>';
 
 		print "$as_prof_name5<br><select name=\"pro_p5\">";
		for($i=0;$i<@as_prof_array5;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p5 eq $as_prof_array5[$i]);
				print ($option,$as_prof_array5[$i]);
		}
		print '</select></td><td>';
		
 		print "$as_prof_name6<br><select name=\"pro_p6\">";
		for($i=0;$i<@as_prof_array6;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p6 eq $as_prof_array6[$i]);
				print ($option,$as_prof_array6[$i]);
		}
		print '</select></td></tr>';
		
		print "<tr><td align=right>一言コメント</td><td colspan=3><input type=text name=pro_p7 size=80 value=$my_prof_hairetu[10]></td></tr>\n";

		print <<"EOM";
	<tr><td colspan=4 align=center>
	<input type=submit value=" この内容で登録する "><br>
	</td></tr></table>
	</form><br>
	<div align=center><form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="touroku_sakujo">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value=" 登録してあるプロフィールを削除する ">
	</form></div>
EOM
	&hooter("assenjo","戻る","kekkon.cgi");
}

###########告白メール
sub kokuhaku {
		if ($love < $need_love){&error("LOVEパラメータが足らないためメールを送ることはできません。");}
		if ($in{'sousinsaki_name'} eq ""){&error("相手先のお名前の入力がありません");}
		if ($in{'m_com'} eq ""){&error("メッセージが入力されていません");}
		$aite_name = "$in{'sousinsaki_name'}";
#koko2007/12/20
	&id_check ($aite_name);
	if ($in{'gift_souhu'}){
		if ($aite_name eq $name){&error("自分に贈ることはできません");}
		&gift_souhu_syori2; #中でロック#koko2006/10/18
	}
#kokoend
		&lock;
#エラーチェック処理
			open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
			eval{ flock (COA, 1); };
			@all_couple = <COA>;
			close(COA);
			$zibun_count = 0;
			$aite_count = 0;
			foreach (@all_couple){
				($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
#cn_yobi1＝次にデートできる日時　cn_yobi2＝最後にしたデート（日時）　cn_yobi3＝その前のデート（日時）cn_yobi4＝最後のデートを誘った人　cn_kodomo＝未使用
				if ($name eq "$cn_name1"){
#結婚OKの場合
					if ($in{'command'} eq "propose_ok"){
						if ($cn_name2 eq "$aite_name"){
							if ($cn_joutai eq "配偶者"){&error("この方はすでにあなたの配偶者です。");}
							$sinkon_number = "$cn_number";
						}
#プロポーズの場合、恋人であるエラーを回避
					}elsif($in{'kokuhaku_syubetu'} eq "propose"){
					
#交際申し込み、交際OKの場合
					}else{
						$zibun_count ++;
						if ($cn_name2 eq "$aite_name"){&error("この方はすでにあなたの$cn_joutaiです。");}
					}
				}
				if ($name eq "$cn_name2"){
#結婚OKの場合
					if ($in{'command'} eq "propose_ok"){
						if ($cn_name1 eq "$aite_name"){
							if ($cn_joutai eq "配偶者"){&error("この方はすでにあなたの配偶者です。");}
							$sinkon_number = "$cn_number";
						}
#プロポーズの場合、恋人であるエラーを回避
					}elsif($in{'kokuhaku_syubetu'} eq "propose"){
#交際OKの場合
					}else{
						$zibun_count ++;
						if ($cn_name1 eq "$aite_name"){&error("この方はすでにあなたの$cn_joutaiです。");}
					}
				}
#相手の名前があった場合
				if ($aite_name eq "$cn_name1" || $aite_name eq "$cn_name2"){
#結婚OKで相手が結婚していたらエラー表示
					if ($in{'command'} eq "propose_ok" && $cn_joutai eq "配偶者"){
						&error("この方は既に結婚しています。	");
					}
#プロポーズの場合、相手が結婚していたらエラー表示
					if($in{'kokuhaku_syubetu'} eq "propose" && $cn_joutai eq "配偶者"){
						&error("この方は既に結婚しています。	");
					}
					$aite_count ++;
				}
			}		#foreach閉じ
			
#結婚OKの場合、恋人かどうかのチェック
		if ($in{'command'} eq "propose_ok"){
			if ($sinkon_number eq ""){&error("二人は恋人ではありません。");}
#プロポーズの場合、恋人であるエラーを回避		#ver.1.30
		}elsif($in{'kokuhaku_syubetu'} eq "propose"){		#ver.1.30
#交際申し込み、交際OKの場合の恋人人数チェック
		}else{
			if($zibun_count >= $koibito_seigen){&error("$nameさんはすでに$koibito_seigen人の方とつき合っているため新たに恋人は作れません。");}
			if($aite_count >= $koibito_seigen){&error("$aite_nameさんはすでに$koibito_seigen人の方とつき合っているため新たに恋人は作れません。");}
		}

		open(PR,"< $as_profile_file") || &error("Open Error : $as_profile_file");
		eval{ flock (PR, 1); };
		@alldata=<PR>;
		close(PR);
		$zibunatta_flg = 0;
		$aiteatta_flg = 0;
		foreach (@alldata){
			($pro_name,$pro_sex)= split(/<>/);
			if ($name eq "$pro_name"){$zibunatta_flg = 1;}
			if ($aite_name eq "$pro_name"){$aiteatta_flg = 1;}
		}
		if ($zibunatta_flg == 0){&error("$nameさんは恋人斡旋所に登録されていません。");}
		if ($aiteatta_flg == 0){&error("$aite_nameさんは恋人斡旋所に登録されていません。");}

#告白メール送信
		&id_check ($aite_name);
			if ($aite_name eq $name){&error("自分に告白することはできません");}
			$message_file="./member/$return_id/mail.cgi";
			open(AIT,"< $message_file") || &error("お相手の方のメール記録ファイル（$message_file）が開けません。");
			eval{ flock (AIT, 1); };
			$last_mail_check_time = <AIT>;
			@mail_cont = <AIT>;
			close(AIT);
#<>禁止処理
		$in{'m_com'} =~ s/<>/&lt;&gt;/g;
# コメントの改行処理
		$in{'m_com'} =~ s/\r\n/<br>/g;
		$in{'m_com'} =~ s/\r/<br>/g;
		$in{'m_com'} =~ s/\n/<br>/g;
		if ($in{'gift_souhu'}){$pulezent="<br><br>$in{'gift_souhu'}をもらいました。"}#koko2007/12/20
		$m_comment = "$in{'m_com'}$pulezent";#koko2007/12/20
		&time_get;
		if ($in{'command'} eq "kousai_ok"){
			$new_mail = "交際承諾受信<>$in{'name'}<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
		}elsif ($in{'command'} eq "propose_ok"){
			$new_mail = "プロポ承諾受信<>$in{'name'}<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
		}elsif ($in{'kokuhaku_syubetu'} eq "propose"){
			$new_mail = "プロポ受信<>$in{'name'}<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
		}else{
			$new_mail = "告白受信<>$in{'name'}<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
		}
			unshift (@mail_cont,$new_mail);
#最終メールチェック時間がなければ１を入れる
			if ($last_mail_check_time eq ""){$last_mail_check_time = "1\n";}
			unshift (@mail_cont,$last_mail_check_time);
			
#自分のメールにも送信済みメッセージとして記録（管理者メールでなければ）
		if ($in{'command'} ne "from_system"){
			$my_sousin_file="./member/$k_id/mail.cgi";
			open(ZIB,"< $my_sousin_file") || &error("$my_sousin_fileが開けません。");
			eval{ flock (ZIB, 1); };
			$my_last_mail_check_time = <ZIB>;
			@my_mail_cont = <ZIB>;
			close(ZIB);
		if ($in{'gift_souhu'}){$pulezent="<br><br>$in{'gift_souhu'}をプレゼントしました。"}#koko2007/12/20
		$my_m_comment = "$in{'m_com'}$pulezent";#koko2007/12/20
		if ($in{'command'} eq "kousai_ok"){
			$sousin_mail = "交際承諾送信<>$aite_name<>$my_m_comment<>$date2<><><><><><><>\n";
		}elsif ($in{'command'} eq "propose_ok"){
			$sousin_mail = "プロポ承諾送信<>$aite_name<>$my_m_comment<>$date2<><><><><><><>\n";
		}elsif ($in{'kokuhaku_syubetu'} eq "propose"){
			$sousin_mail = "プロポ送信<>$aite_name<>$my_m_comment<>$date2<><><><><><><>\n";
		}else{
			$sousin_mail = "告白送信<>$aite_name<>$my_m_comment<>$date2<><><><><><><>\n";
		}
			unshift (@my_mail_cont,$sousin_mail);
#最終メールチェック時間がなければ今の時間を入れる
			if ($my_last_mail_check_time eq ""){$my_last_mail_check_time = "$date_sec\n";}
			unshift (@my_mail_cont,$my_last_mail_check_time);
		
#相手のメールログへの書き込み処理
			open(OUT,">$message_file") || &error("$message_fileに書き込めません");
			eval{ flock (OUT, 2); };
			print OUT @mail_cont;
			close(OUT);
#自分のメールログへ書き込み処理
			open(ZIBO,">$my_sousin_file") || &error("$my_sousin_fileに書き込めません");
			eval{ flock (ZIBO, 2); };
			print ZIBO @my_mail_cont;
			close(ZIBO);

#交際返事の場合の恋愛ログ更新
			if ($in{'command'} eq "kousai_ok"){
				&couple_kiroku($name,$aite_name,"恋人","");
#名前１,名前２,状態,カップル番号
#街のニュースに記録
				&news_kiroku("恋人","$nameさんと$aite_nameさんが恋人になりました。");
#結婚返事の場合の恋愛ログ更新
			}elsif ($in{'command'} eq "propose_ok"){
				&couple_kiroku($name,$aite_name,"結婚","$sinkon_number");
				&news_kiroku("結婚","$nameさんと$aite_nameさんが結婚しました。");
#相手の個人ログの配偶者IDに自分のIDを記録
					&id_check($aite_name);
					&openAitelog ($return_id);
					$aite_house_type = "$k_id";
					&aite_temp_routin;
				open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
				eval{ flock (OUT, 2); };
				print OUT $aite_k_temp;
				close(OUT);
			}
		}
		&unlock;
#結婚の場合自分の個人ログに配偶者IDを記録
		if ($in{'command'} eq "propose_ok"){
			$house_type = "$return_id";
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
		}
		if ($in{'command'} eq "kousai_ok"){
			&message_only("$aite_nameさんと恋人になりました。");
			&hooter("mail_sousin","メール画面へ");
			&hooter("login_view","戻る");
		}elsif ($in{'command'} eq "propose_ok"){
			&message_only("$aite_nameさんと結婚しました。");
			&hooter("mail_sousin","メール画面へ");
			&hooter("login_view","戻る");
		}elsif ($in{'kokuhaku_syubetu'} eq "propose"){
			&message_only("$aite_nameさんにプロポーズしました。");
			&hooter("renai","戻る","kekkon.cgi");
		}else{
			&message_only("$aite_nameさんに告白しました。");
			&hooter("assenjo","戻る","kekkon.cgi");
		}
	exit;
}

#恋愛ログの記録
sub couple_kiroku {
#結婚成立の場合
				if (@_[2] eq "結婚"){
					open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
					eval{ flock (COA, 1); };
						@all_couple = <COA>;
					close(COA);
					foreach (@all_couple){
						($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
						if (@_[3] eq "$cn_number"){
							$cn_joutai = "配偶者";
						}
						$couple_tmp = "$cn_number<>$cn_name1<>$cn_name2<>$cn_joutai<>$cn_total_aijou<>$cn_omoide1<>$cn_omoide2<>$cn_omoide3<>$cn_omoide4<>$cn_omoide5<>$cn_kodomo<>$cn_yobi1<>$cn_yobi2<>$cn_yobi3<>$cn_yobi4<>$cn_yobi5<>\n";
						push (@new_all_couple,$couple_tmp);
					}
						open(COP,">$couple_file") || &error("$couple_fileに書き込めません");
						eval{ flock (COP, 2); };
						print COP @new_all_couple;
						close(COP);
#恋人成立の場合
				}elsif (@_[2] eq "恋人"){
					open(CO,"< $couple_file") || &error("$couple_fileに書き込めません");
					eval{ flock (CO, 1); };
					$last_couple = <CO>;
					@couple_news = <CO>;
						($new_cn_number,$cn_name1,$cn_name2,$cn_joutai)= split(/<>/,$last_couple);
						$new_cn_number ++;
					close(CO);
					$now_time = time;
					$new_couple_tmp = "$new_cn_number<>@_[0]<>@_[1]<>恋人<>0<>0<>0<>0<>0<>0<>0<>$now_time<><><><><>\n";
					unshift (@couple_news,$last_couple);
					unshift (@couple_news,$new_couple_tmp);
					
					open(COP,">$couple_file") || &error("$couple_fileに書き込めません");
					eval{ flock (COP, 2); };
					print COP @couple_news;
					close(COP);
				}
}

#恋愛コマンド
sub renai {
	open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
	eval{ flock (COA, 1); };
		@all_couple = <COA>;
	close(COA);
		
	open(REN,"< ./dat_dir/love.cgi") || &error("Open Error : ./dat_dir/love.cgi");
	eval{ flock (REN, 1); };
	$top_koumoku = <REN>;
	@date_hairetu = <REN>;
	close(REN);
	my (@koumokumei_hairetu)= split(/<>/,$top_koumoku);
#デートの場合
	if ($in{'command'} eq "do_date"){
		$dekityatta = 0;
		$date_aite_iru_flg=0;
		foreach (@all_couple){
			($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
			if ($cn_number eq "$in{'date_aite'}"){
				$date_aite_iru_flg=1;
				if ($name eq "$cn_yobi4"){&error("次は相手の方がデートに誘う番です。");}
				&time_get;
				if ($cn_yobi1 > $date_sec){&error("まだデートできません。");}
				if ($name eq "$cn_name1"){$aitenonamae = "$cn_name2";}
				else{$aitenonamae = "$cn_name1";}
				foreach  (@date_hairetu) {
					my ($date_name,$date_dousi,$date_tanosii,$date_h,$date_omosiroi,$date_kandou,$date_oisii,$date_hiyou,$date_kankaku,$kodomo_kakuritu)= split(/<>/);
					if ($date_name eq "$in{'date_koumoku'}"){
							$date_comment .= "$aitenonamaeさんと$date_dousi<br>";
							if ($date_tanosii){$cn_omoide1 += $date_tanosii; $date_comment .= "$koumokumei_hairetu[2]が$date_tanosii増えました。<br>";}
							if ($date_h){$cn_omoide2 += $date_h; $date_comment .= "$koumokumei_hairetu[3]が$date_h増えました。<br>";}
							if ($date_omosiroi){$cn_omoide3 += $date_omosiroi; $date_comment .= "$koumokumei_hairetu[4]が$date_omosiroi増えました。<br>";}
							if ($date_kandou){$cn_omoide4 += $date_kandou; $date_comment .= "$koumokumei_hairetu[5]が$date_kandou増えました。<br>";}
							if ($date_oisii){$cn_omoide5 += $date_oisii; $date_comment .= "$koumokumei_hairetu[6]が$date_oisii増えました。<br>";}
					if ($in{'siharaihouhou'} ne "現金"){
						$bank -= $date_hiyou;
						&kityou_syori("クレジット支払い（デート費用）","$date_hiyou","",$bank,"普");
					}else{
						if ($money < $date_hiyou){&error("お金が足りません");}
						$money -= $date_hiyou;
					}
							$cn_yobi1= $date_sec + (60*60*$date_kankaku);		#次にデートできる時間
							$cn_yobi3 = "$cn_yobi2";		#一つ前のデート
							$cn_yobi2 = "$date_dousi（$date2）";		#最後のデート
#子供が生まれるイベント
							if ($kodomo_kakuritu == 1){
								if ($cn_joutai eq "配偶者"){
									$ko_randed=int(rand($kodomo_kakuritu1)+1);
								}elsif ($cn_joutai eq "恋人"){
									$ko_randed=int(rand($kodomo_kakuritu2)+1);
								}
								if ($cn_joutai eq "配偶者" && $ko_randed == int($kodomo_kakuritu1 / 2)+1){		#子供が生まれた場合koko2007/12/14
									$dekityatta = 1;
								}elsif($cn_joutai eq "恋人" && $ko_randed == int($kodomo_kakuritu2/2)+1){
									$dekityatta = 1;
								}
#koko2007/11/25
								if($dekityatta){
									if($kodomo_seibetu eq 'yes'){
										$ko_sex=int(rand(2));
										if($ko_sex ==0){
											$ko_sex="m";
											$ko_sex_setu="元気な男の子";
											$syutu = '男出産';
										}else{
											$ko_sex="f";
											$ko_sex_setu="可愛い女の子";
											$syutu = '女出産';
										}
									}else{
										$ko_sex="";
										$ko_sex_setu="";
										$syutu = '出産';
									}

									$cn_yobi2 = "$date_dousi<span class=mainasu>$ko_sex_setuができました！</span>（$date2）";
									$date_comment .= "<div class=mainasu>おめでとうございます！！<br>二人の間に$ko_sex_setuの赤ちゃんが産まれました！<br>子供の名前を決めるための書類をメールでお送りしましたのでご覧ください。</div>";
#kokoend
#									$date_comment .= "<div class=mainasu>おめでとうございます！<br>二人の間に子供ができました！<br>子供の名前を決めるための書類をメールでお送りしましたのでご覧ください。</div>";
								}
							}
							$cn_yobi4 = "$name";				#誘った人
							$cn_total_aijou = $cn_omoide1 + $cn_omoide2 + $cn_omoide3 + $cn_omoide4 + $cn_omoide5;
							last;
					}		#デート内容一致の場合の閉じ
				}		#デート内容foreachの閉じ
			}		#カップル番号一致の閉じ
			$date_tmp = "$cn_number<>$cn_name1<>$cn_name2<>$cn_joutai<>$cn_total_aijou<>$cn_omoide1<>$cn_omoide2<>$cn_omoide3<>$cn_omoide4<>$cn_omoide5<>$cn_kodomo<>$cn_yobi1<>$cn_yobi2<>$cn_yobi3<>$cn_yobi4<>$cn_yobi5<>\n";
			push (@new_all_couple,$date_tmp);
		}		#カップル番号foreach閉じ
		if ($date_aite_iru_flg==0){&error("デート相手が見つかりません。");}

#ログ更新
		&lock;
#子供ができた場合
		if ($dekityatta == 1){
			&time_get;
			open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
			eval{ flock (KOD, 1); };
			$last_kodomo = <KOD>;
			@all_kodomo=<KOD>;
			close(KOD);
			($kod_num,$kod_name)= split(/<>/,$last_kodomo);
			$kod_num ++;
			$date_sec_tmp = $date_sec - (60*60*$kosodate_kankaku);
			$new_kodomo_temp = "$kod_num<><>$name<>$aitenonamae<><>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>$date_sec_tmp<>$date_sec_tmp<><><>50<>3<>$date_sec_tmp<><><>$ko_sex<>\n";#koko2007/11/25
			unshift (@all_kodomo,$last_kodomo);
			unshift (@all_kodomo,$new_kodomo_temp);
#子供の名前を決めるメール送信
			$my_sousin_file="./member/$k_id/mail.cgi";
			open(ZIB,"< $my_sousin_file") || &error("$my_sousin_fileが開けません。");
			eval{ flock (ZIB, 1); };
			$my_last_mail_check_time = <ZIB>;
			@my_mail_cont = <ZIB>;
			close(ZIB);
			$sousin_mail = "$syutu<>$aitenonamae<>$kod_num<>$date2<>$date_sec<><><><><><>\n"; #koko2007/11/25
			unshift (@my_mail_cont,$sousin_mail);
			unshift (@my_mail_cont,$my_last_mail_check_time);
			
#メールログ更新
			open(ZIBO,">$my_sousin_file") || &error("$my_sousin_fileに書き込めません");
			eval{ flock (ZIBO, 2); };
			print ZIBO @my_mail_cont;
			close(ZIBO);
#子供ログ更新
		open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
		eval{ flock (KODO, 2); };
		print KODO @all_kodomo;
		close(KODO);
		}		#子供ができた場合閉じ
#カップルログ更新
		open(COP,">$couple_file") || &error("$couple_fileに書き込めません");
		eval{ flock (COP, 2); };
		print COP @new_all_couple;
		close(COP);
		&unlock;
#個人ログ更新
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
		
	&header("","sonomati");
		print <<"EOM";
		<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
	<span class="job_messe">
	$date_comment
	</span>
	</td></tr></table>
	<br>
EOM
			&hooter("renai","恋愛画面へ","kekkon.cgi");
			&hooter("login_view","戻る");
	exit;
	}		#デートの場合閉じ
#ラブラブ度順にソート
#	foreach (@all_couple){
#			$data=$_;
#koko2006/03/11
#			$key=(split(/<>/,$data))[4];		#ソートする要素を選ぶ
#			push @all_couple_sort,$data;
#			push @keys,$key;
#	}
#		sub bykeys{$keys[$b] <=> $keys[$a];}
#		@all_couple_sort=@all_couple_sort[ sort bykeys 0..$#all_couple_sort]; 
		@all_couple_sort = @all_couple;
		@keys0 = map {(split /<>/)[4]} @all_couple_sort;
		@all_couple_sort = @all_couple_sort[sort {@keys0[$a] cmp @keyso[$b]} 0 .. $#keys0];
#kokoend2006/03/11

	&header(assen_style);
		print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●恋人や配偶者ができるとこちらでデートすることができます。ただし、デートは二人が交互に誘う必要があります。<br>
	●デートによって二人の思い出を増やしていき、ラブラブ度（思い出数値の合計）が$aijou_kijunを超え、さらに全ての思い出数値が最低基準の$omoide_kijunを超えていれば結婚の申\し込みができるようになります。<br>
	●自分、またはお相手に配偶者がいる場合は結婚できません。<br>
	●結婚後は、配偶者が住んでいる家の各種設定やお店の仕入れなどを共同でできるようになります（二人とも家を持っている場合も、家を手放す必要はありません）。<br>
	●恋人の場合$wakare_limit_koibito日間、配偶者の場合は$wakare_limit_haiguu日間デートをしないと二人は別れてしまいます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">恋　愛</div>
EOM
#koko2007/06/22
		if ($kapul_disp eq 'yes'){
			print <<"EOM";
	<div align=center><form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="couple_ranking">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="カップルランキング">
	</form></div>
EOM
		}
		print <<"EOM";
	</td></tr></table><br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="renai">
	<input type=hidden name=command value="do_date">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr bgcolor=#ffcc66>
	<td colspan=3 class=honbun3>お相手とデート内容を選んでください。かっこ内は「かかる費用」と「次にデートできるまでの時間」です。<br>
	デートの内容によっては子供ができることがあります（相手が配偶者なら$kodomo_kakuritu1分の１、恋人なら$kodomo_kakuritu2分の１の確率）。</td></tr>
	<tr bgcolor=#ffcc66><td align=right>
	お相手 <select name="date_aite">
EOM
	my (@my_koibito_hairetu,$my_haiguusya_hairetu);
	$koibito_iru = 0;
	foreach (@all_couple_sort){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
		if ($name eq "$cn_name1"){
				if ($cn_joutai eq "恋人"){
					push (@my_koibito_hairetu,$_);
					print "<option value=\"$cn_number\">$cn_name2</option>";
				}elsif ($cn_joutai eq "配偶者"){
					$my_haiguusya_hairetu = "$_";
					print "<option value=\"$cn_number\">$cn_name2</option>";
				}
				$koibito_iru ++; 
		}
		if ($name eq "$cn_name2"){
				if ($cn_joutai eq "恋人"){
					push (@my_koibito_hairetu,$_);
					print "<option value=\"$cn_number\">$cn_name1</option>";
				}elsif ($cn_joutai eq "配偶者"){
					$my_haiguusya_hairetu = "$_";
					print "<option value=\"$cn_number\">$cn_name1</option>";
				}
				$koibito_iru ++; 
		}
	}
	if ($koibito_iru == 0){
		print "<option value=\"\">現在つき合っている方はいません</option>";
	}
	print <<"EOM";
	</selct></td><td align=center>
	デート内容 <select name="date_koumoku">
EOM
	foreach  (@date_hairetu) {
		my ($date_name,$date_dousi,$date_tanosii,$date_h,$date_omosiroi,$date_kandou,$date_oisii,$date_hiyou,$date_kankaku)= split(/<>/);
		print <<"EOM";
	<option value="$date_name">$date_name（$date_hiyou円、$date_kankaku時間）</option>
EOM
	}
	print "</select></td><td>";
	
#所有物チェック
	if(!$k_id){&error("mono.cgi エラー kekkon1")} #koko2007/11/18
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
#koko2007/12/20
	foreach (@my_kounyuu_list){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "ギフト"){
			$gift_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
	}
#kokoend
	print <<"EOM";
	支払い <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
	<input type=submit value=" O K ">
	</td></tr>
	</table></form>
EOM

#配偶者の表示
	if ($my_haiguusya_hairetu ne ""){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/,$my_haiguusya_hairetu);
		if ($cn_name1 eq $name){$haiguusya_name = $cn_name2;}else{$haiguusya_name = $cn_name1;}
		if ($cn_yobi1 < time){$next_d = "<span class=purasu> O K </span>";}else{&byou_hiduke($cn_yobi1);$next_d = "<span class=mainasu>$bh_full_date</span>";}
	print <<"EOM";
	<div class=honbun4 align=center>＜$nameさんの配偶者＞</div>
	<table width="90%" border="0" cellspacing="0" cellpadding="6" align=center class=yosumi>
	<tr bgcolor=#ffffaa>
	<td style="font-size:12px;color:ff3300" width=90 nowrap>$haiguusya_name</td>
	<td><span class=honbun2>ラブラブ度：$cn_total_aijou</span></td>
	<td><span class=honbun2>$koumokumei_hairetu[2]：</span>$cn_omoide1</td>
	<td><span class=honbun2>$koumokumei_hairetu[3]：</span>$cn_omoide2</td>
	<td><span class=honbun2>$koumokumei_hairetu[4]：</span>$cn_omoide3</td>
	<td><span class=honbun2>$koumokumei_hairetu[5]：</span>$cn_omoide4</td>
	<td><span class=honbun2>$koumokumei_hairetu[6]：</span>$cn_omoide5</td></tr>
	<tr bgcolor=#ffffaa><td colspan=7><hr size=1><span class=honbun2>次にデートできる時間：</span>$next_d<br>
	<span class=honbun2>最後にしたデート：</span>$cn_yobi2<span class=purasu>$cn_yobi4さんが誘いました。</span><br>
	<span class=honbun2>ひとつ前のデート：</span>$cn_yobi3<br>
	<form method="POST" action="$script">
	<input type=hidden name=mode value="mail_do">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type=hidden name=sousinsaki_name value="$haiguusya_name">
	メッセージ <textarea rows=2 name=m_com cols=50 ></textarea>
	<input type="submit" value=" メールを送る ">
	</form>
	</td></tr>
<!--	<tr bgcolor=#ffffaa><td colspan=7>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="wakare">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type=hidden name=sousinsaki_name value="$haiguusya_name">
	<input type="submit" value=" 分かれる ">
	</form>
	</td></tr>-->

</table><br><br>
EOM
	}		#配偶者がいる場合の閉じ
#恋人の表示
	if (@my_koibito_hairetu != ""){print "<div class=honbun4 align=center>＜$nameさんの恋人＞</div>";}
	foreach  (@my_koibito_hairetu) {
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
		if ($cn_name1 eq $name){$koibito_name = $cn_name2;}else{$koibito_name = $cn_name1;}
		if ($cn_yobi1 < time){$next_d = "<span class=purasu> O K </span>";}else{&byou_hiduke($cn_yobi1);$next_d = "<span class=mainasu>$bh_full_date</span>";}
		if ($cn_yobi4 ne ""){$sasoi_aite_folo = "さんが誘いました。";}else{$sasoi_aite_folo = "";}
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="6" align=center class=yosumi>
	<tr bgcolor=#ffffff>
	<td style="font-size:12px;color:ff3300" width=90 nowrap>$koibito_name</td>
	<td><span class=honbun2>ラブラブ度：$cn_total_aijou</span></td>
	<td><span class=honbun2>$koumokumei_hairetu[2]：</span>$cn_omoide1</td>
	<td><span class=honbun2>$koumokumei_hairetu[3]：</span>$cn_omoide2</td>
	<td><span class=honbun2>$koumokumei_hairetu[4]：</span>$cn_omoide3</td>
	<td><span class=honbun2>$koumokumei_hairetu[5]：</span>$cn_omoide4</td>
	<td><span class=honbun2>$koumokumei_hairetu[6]：</span>$cn_omoide5</td></tr>
	<tr><td colspan=7><hr size=1><span class=honbun2>次にデートできる時間：</span>$next_d<br>
	<span class=honbun2>最後にしたデート：</span>$cn_yobi2<span class=purasu>$cn_yobi4$sasoi_aite_folo</span><br>
	<span class=honbun2>ひとつ前のデート：</span>$cn_yobi3<br>
	<form method="POST" action="$script">
	<input type=hidden name=mode value="mail_do">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=sousinsaki_name value="$koibito_name">
	メッセージ <textarea rows=2 name=m_com cols=50 ></textarea>
	<input type="submit" value=" メールを送る ">
	</form>
	</td></tr>
<!--	<tr><td>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="wakare">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type=hidden name=sousinsaki_name value="$koibito_name">
	<input type="submit" value=" 分かれる ">
	</form>
	</td></tr> -->

EOM
#ラブラブ度と思い出数値が基準を超えていたらプロポーズフォーム出力
	if ($cn_total_aijou >= $aijou_kijun && $cn_omoide1 >= $omoide_kijun && $cn_omoide2 >= $omoide_kijun && $cn_omoide3 >= $omoide_kijun && $cn_omoide4 >= $omoide_kijun && $cn_omoide5 >= $omoide_kijun && $my_haiguusya_hairetu eq ""){
	print <<"EOM";
	 <tr bgcolor=#ffcccc><td colspan=7><form method="POST" action="$this_script">
	<input type=hidden name=mode value="kokuhaku">
	<input type=hidden name=kokuhaku_syubetu value="propose">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name="sousinsaki_name" value="$koibito_name">
	<span class=mainasu>プロポーズの言葉</span> <textarea rows=2 name=m_com cols=50 ></textarea>
	<input type=submit value="結婚を申\し込む">
	●プレゼント送付<!-- koko2007/12/20 -->
	<select name=gift_souhu>
	<option value="">無し</option>
	$gift_select
	</select><br>	
</form>
	</td></tr>
EOM
	}
	print "</table><br><br>";
	}
	&hooter("login_view","街へ戻る");
exit;
}

#子供の名前決め
sub kodomo_naming {
	open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
	eval{ flock (KOD, 1); };
	@all_kodomo=<KOD>;
	close(KOD);
	@new_all_kodomo = ();
	$kodomoatta_flg = 0;
	$umu_news = "0";
	foreach (@all_kodomo){
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
		chomp $kod_renraku1;

		if ($kod_num eq "$in{'kod_num'}"){
			$kodomoatta_flg = 1;
#産む場合
			if ($in{'umu_umanai'} eq "umu"){
				if (length($in{'kodomo_name'}) > 20) {&error("子供の名前は全角10文字以内でお願いします。");}
				if ($kod_name ne ""){&error("すでにこの子には名前がついています。");}
				$kod_name = "$in{'kodomo_name'}";
				$message_in = "「$kod_name」ちゃんが産まれました！";
				$kod_yobi1 = time;
				$umu_news = "1";
#koko2007/11/25
				if($kod_yobi10 eq "m" && $kodomo_seibetu eq 'yes'){$dis_ko_sex = '元気な男の子';$syutu = '男出産';}
				elsif($kod_yobi10 eq "f" && $kodomo_seibetu eq 'yes'){$dis_ko_sex = '可愛い女の子';$syutu = '女出産';}
				else{$dis_ko_sex = '子供';$syutu = '出産';}
				$news_messe = "$kod_oya1さんと$kod_oya2さんとの間に$dis_ko_sexが産まれました。「$kod_name」ちゃんと命名したようです。";
#産まない場合削除
			}elsif($in{'umu_umanai'} eq "umanai"){
				$message_in = "子供をおろしました。";
				$umu_news = "2";
				$news_messe = "$kod_oya1さんと$kod_oya2さんとの間に子供が産まれましたがおろしたようです。";
				next;
			}
		}
		$kodomo_temp = "$kod_num<>$kod_name<>$kod_oya1<>$kod_oya2<>$kod_job<>$kod_kokugo<>$kod_suugaku<>$kod_rika<>$kod_syakai<>$kod_eigo<>$kod_ongaku<>$kod_bijutu<>$kod_looks<>$kod_tairyoku<>$kod_kenkou<>$kod_speed<>$kod_power<>$kod_wanryoku<>$kod_kyakuryoku<>$kod_love<>$kod_unique<>$kod_etti<>$kod_yobi1<>$kod_yobi2<>$kod_yobi3<>$kod_yobi4<>$kod_yobi5<>$kod_yobi6<>$kod_yobi7<>$kod_yobi8<>$kod_yobi9<>$kod_yobi10<>$kod_renraku1<>$kod_renraku2<>\n";
		push (@new_all_kodomo,$kodomo_temp);
	}		#foreach閉じ
	&lock;
	if ($kodomoatta_flg == 0){&error("この子供はすでに出産、または流産しています。");}
#子供ログ更新
	open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
	eval{ flock (KODO, 2); };
	print KODO @new_all_kodomo;
	close(KODO);
#街ニュースに記録
	if ($umu_news == 1){
		&news_kiroku("$syutu","$news_messe");#koko2007/11/25
	} elsif ($umu_news == 2){
#		&news_kiroku("死亡","$news_messe");
	}
	&unlock;
	
	&message_only("$message_in");
	&hooter("mail_sousin","メール画面へ");
	&hooter("login_view","戻る");
	exit;
}

#子育て
sub kosodate {
	open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
	eval{ flock (KOD, 1); };
	@all_kodomo=<KOD>;
	close(KOD);

	if(!$k_id){&error("mono.cgi エラー kekkon2")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
#連絡変更
	if ($in{'command'} eq "renraku"){
		$renraku_taisyou_flg=0;
		foreach (@all_kodomo){
			($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
			chomp $kod_renraku1;
			if ($in{'kod_num'} eq "$kod_num"){
				$renraku_taisyou_flg=1;
				$in{'renraku1'} =~ s/</&lt;/g;
				$in{'renraku1'} =~ s/>/&gt;/g;
				$in{'renraku2'} =~ s/</&lt;/g;
				$in{'renraku2'} =~ s/>/&gt;/g;
				if($in{'renraku1'}){$kod_renraku1 = $in{'renraku1'};}
				if($in{'renraku2'}){$kod_renraku2 = $in{'renraku2'};}
			}
			$new_kodomo_temp = "$kod_num<>$kod_name<>$kod_oya1<>$kod_oya2<>$kod_job<>$kod_kokugo<>$kod_suugaku<>$kod_rika<>$kod_syakai<>$kod_eigo<>$kod_ongaku<>$kod_bijutu<>$kod_looks<>$kod_tairyoku<>$kod_kenkou<>$kod_speed<>$kod_power<>$kod_wanryoku<>$kod_kyakuryoku<>$kod_love<>$kod_unique<>$kod_etti<>$kod_yobi1<>$kod_yobi2<>$kod_yobi3<>$kod_yobi4<>$kod_yobi5<>$kod_yobi6<>$kod_yobi7<>$kod_yobi8<>$kod_yobi9<>$kod_yobi10<>$kod_renraku1<>$kod_renraku2<>\n";
			push (@new_all_kodomo,$new_kodomo_temp);
		}	#foreach閉じ
		if ($renraku_taisyou_flg==0){&error("対象の子供が見つかりません。");}
#子供ログ更新
		&lock;
		open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
		eval{ flock (KODO, 2); };
		print KODO @new_all_kodomo;
		close(KODO);
		&unlock;
	}

#パラメータアップの場合
	if ($in{'command'} eq "do_kosodate"){
		$sodate_taisyou_flg=0;
		foreach (@all_kodomo){
			($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
			chomp $kod_renraku1;
#$kod_num<>$kod_name<>$kod_oya1<>$kod_oya2<>$kod_job<>$kod_kokugo<>$kod_suugaku<>$kod_rika<>$kod_syakai<>$kod_eigo<>$kod_ongaku<>$kod_bijutu<>$kod_looks<>$kod_tairyoku<>$kod_kenkou<>$kod_speed<>$kod_power<>$kod_wanryoku<>$kod_kyakuryoku<>$kod_love<>$kod_unique<>$kod_etti<>$kod_yobi1<>$kod_yobi2<>$kod_yobi3<>$kod_yobi4<>$kod_yobi5<>$kod_yobi6<>$kod_yobi7<>$kod_yobi8<>$kod_yobi9<>$kod_yobi10
#kod_yobi1＝出産時間（秒）kod_yobi2＝最後に子育てした時間　kod_yobi3＝最後の子育てコメント　kod_yobi4＝トータル能力値　kod_yobi5＝身長　kod_yobi6＝体重　kod_yobi7＝最後の食事時間　kod_yobi8＝自立フラグ　kod_yobi9＝最後に子育てした人
		if ($in{'kod_num'} eq "$kod_num"){
			$sodate_taisyou_flg=1;
			&time_get;
			if (($date_sec - $kod_yobi2) < (60*60*$kosodate_kankaku)){&error("まだ子育てできません。");}
			if ($kod_yobi9  eq "$name"){&error("次は配偶者の方が子育てする番です。");}
			$konoagatta_suuti = int($in{'par_suuti'}/$kosodatewaruatai); #koko2006/12/02
			if ($in{'nouryoku'} eq "国語") { $kod_kokugo += $konoagatta_suuti; $kokugo -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "数学") { $kod_suugaku += $konoagatta_suuti; $suugaku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "理科") { $kod_rika += $konoagatta_suuti; $rika -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "社会") { $kod_syakai += $konoagatta_suuti; $syakai -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "英語") { $kod_eigo += $konoagatta_suuti; $eigo -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "音楽") { $kod_ongaku += $konoagatta_suuti; $ongaku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "美術") { $kod_bijutu += $konoagatta_suuti; $bijutu -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "体力") { $kod_tairyoku += $konoagatta_suuti; $tairyoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "健康") { $kod_kenkou += $konoagatta_suuti; $kenkou -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "スピード") { $kod_speed += $konoagatta_suuti; $speed -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "パワー") { $kod_power += $konoagatta_suuti; $power -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "腕力") { $kod_wanryoku += $konoagatta_suuti; $wanryoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "脚力") { $kod_kyakuryoku += $konoagatta_suuti; $kyakuryoku -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "ルックス") { $kod_looks += $konoagatta_suuti; $looks -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "LOVE") { $kod_love += $konoagatta_suuti; $love -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "面白さ") { $kod_unique += $konoagatta_suuti; $unique -=$in{'par_suuti'}; }
			elsif ($in{'nouryoku'} eq "エッチ") { $kod_etti += $konoagatta_suuti; $etti -=$in{'par_suuti'}; }
			elsif ($in{'syokuryou'}) {
				$syouhinattaflg = 0;

				@new_myitem_hairetu =(); #koko2007/06/05
				foreach (@my_kounyuu_list){
					&syouhin_sprit($_);
					if ($in{'syokuryou'} eq "$syo_hinmoku"){
#年齢別掛け率を算出
						$kono_nenrei = int (($now_time - $kod_yobi1)/(60*60*24));
						if ($kono_nenrei >= 16){$nenreibetu_kakeritu =0.8;}
						elsif  ($kono_nenrei >= 14){$nenreibetu_kakeritu =1;}
						elsif  ($kono_nenrei >= 10){$nenreibetu_kakeritu =1.2;}
						elsif  ($kono_nenrei >= 5){$nenreibetu_kakeritu =1.5;}
						elsif  ($kono_nenrei >= 3){$nenreibetu_kakeritu =2.5;}
						else {$nenreibetu_kakeritu =3.5;}
						$syouhinattaflg = 1;
						$kod_taijuu_hue = $nenreibetu_kakeritu * ($syo_cal / 1000);
						$kod_yobi6 += $kod_taijuu_hue;
						$randed = (int (rand(10)+10))/10;
						$sintyouup = $randed * (($syo_tairyoku + $syo_kenkou + $syo_speed + $syo_power + $syo_wanryoku + $syo_kyakuryoku)/10);
						$kod_yobi5 += $nenreibetu_kakeritu * $sintyouup ;
						$kod_sintyou_hue = $nenreibetu_kakeritu * $sintyouup ;#koko 2005/05/31
						if ($syo_taikyuu_tani eq "回"){$syo_taikyuu -- ;}
						$kod_yobi7 = $date_sec;
					}		#商品が見つかった場合
					if ($syo_taikyuu <= 0){next;}
					&syouhin_temp;
					push (@new_myitem_hairetu,$syo_temp);
				}		#foreach閉じ
				if ($syouhinattaflg == 0){&error("商品がありません。");}
			}else{&error("指示が不明確です。");}		#食事の場合閉じ
				if ($kokugo < 0 || $suugaku < 0 || $rika < 0 || $syakai < 0 || $eigo < 0 || $ongaku < 0 || $bijutu < 0 || $looks < 0 || $tairyoku < 0 || $kenkou < 0 || $speed < 0 || $power < 0 || $wanryoku < 0 || $kyakuryoku < 0 || $love < 0 || $unique < 0 || $etti < 0){&error("パラメータが足りません。親はすべてのパラメータにおいてプラスである必要があります。");}
#最後の子育て時間を更新
			$kod_yobi2 = $date_sec;
#最後に子育てした人を記録
			$kod_yobi9 = "$name";
#食事の場合
			if ($in{'syokuryou'}){
				&check_BMI($kod_yobi5,$kod_yobi6);#koko 2005/05/31
				$kod_yobi3 = "$nameさんが子供に$in{'syokuryou'}を食べさせました（$date2）";
				$message_in ="$kod_nameちゃんに$in{'syokuryou'}を食べさせました。<br>身長：$kod_yobi5 cm $kod_sintyou_hue cm UP<br>体重：$kod_yobi6 kg $kod_taijuu_hue kg UP<br>体格指数：$BMI（$taikei）"; #koko 2005/05/31
#パラメータアップの場合
			}else{
				$youikuhi = $konoagatta_suuti * $youikuhiyou;
				$kod_yobi3 = "$nameさんが子供の$in{'nouryoku'}パラメータを$konoagatta_suutiあげました（$date2）";
				$message_in ="$kod_nameちゃんの$in{'nouryoku'}パラメータが$konoagatta_suutiあがりました。養育費として$youikuhi円かかりました。";
				#koko
				if ($in{'siharaihouhou'} ne "現金"){
					$bank -= $youikuhi;
					&kityou_syori("クレジット支払い（養育費用）","$youikuhi","",$bank,"普");
				}else{
					if ($money < $date_hiyou){&error("お金が足りません");}
					$money -= $youikuhi;
				}
				#$money -= $youikuhi;
				#kokoend
			}
#総合能力値計算
				$sogo_sisuu = ($kod_yobi5 + $kod_yobi6)/50;
				$kod_yobi4 = int (($kod_kokugo + $kod_suugaku + $kod_rika + $kod_syakai + $kod_eigo + $kod_ongaku + $kod_bijutu + $kod_looks + $kod_tairyoku + $kod_kenkou + $kod_speed + $kod_power + $kod_wanryoku + $kod_kyakuryoku + $kod_love + $kod_unique + $kod_etti)*$sogo_sisuu);
				
			}		#子供番号一致の場合閉じ
			$new_kodomo_temp = "$kod_num<>$kod_name<>$kod_oya1<>$kod_oya2<>$kod_job<>$kod_kokugo<>$kod_suugaku<>$kod_rika<>$kod_syakai<>$kod_eigo<>$kod_ongaku<>$kod_bijutu<>$kod_looks<>$kod_tairyoku<>$kod_kenkou<>$kod_speed<>$kod_power<>$kod_wanryoku<>$kod_kyakuryoku<>$kod_love<>$kod_unique<>$kod_etti<>$kod_yobi1<>$kod_yobi2<>$kod_yobi3<>$kod_yobi4<>$kod_yobi5<>$kod_yobi6<>$kod_yobi7<>$kod_yobi8<>$kod_yobi9<>$kod_yobi10<>$kod_renraku1<>$kod_renraku2<>\n";
			push (@new_all_kodomo,$new_kodomo_temp);
		}	#foreach閉じ
		if ($sodate_taisyou_flg==0){&error("対象の子供が見つかりません。");}
#子供ログ更新
		&lock;
		open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
		eval{ flock (KODO, 2); };
		print KODO @new_all_kodomo;
		close(KODO);
#自分の所有物ファイルを更新
		if ($in{'syokuryou'}){
			open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close(OUT);
#koko2006/11/27
			$loop_count = 0;
			while ($loop_count <= 10){
				for (0..50){$i=0;}#koko2007/06/19
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
		}
		&unlock;
#個人ログ更新
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);

			&message_only("$message_in");
			&hooter("kosodate","子育て画面へ","kekkon.cgi");
			&hooter("login_view","戻る");
	exit;
	}		#パラメータアップの場合閉じ

#所有物チェック koko
	if(!$k_id){&error("mono.cgi エラー kekkon3")} #koko2007/11/18
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
	#kokoend

	if($in{'para'} eq 'on'){
		$disp_para = '<iframe src="./syokugyo.htm" name="syokugyo" width="90%" height="250px" align=center></iframe>';
		$checked = ' checked';
	}

	&header(assen_style);
#koko2006/11/30 syokugyo.htm
		print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>●自分の持っているパラメータを子供のために使ったり、食料品を与えることで子育てができます。ただしお相手と交互にしかできません。<br>
	●食事は身長と体重に影響を与えますが、パラメータには関係しません。<br>
	●子供は与えたパラメータの10分の1しか得ることができません。<br>
	●子供のパラメータ１に対して$youikuhiyou円の養育費がかかります。<br>
	●子育てできる間隔は$kosodate_kankaku時間です。<br>
	●子供は１日１歳ずつ歳をとり、19歳になると自立して親元からいなくなります。自立後は稼ぎに応じた仕送りを一定期間するようになります。<br>
	●$kodomo_sibou_time日間、食事させないと子供は死んでしまいます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">子育て</div>
	<div align=center><form method="POST" action="$this_script">
	<input type=hidden name=mode value="assenjo">
	<input type=hidden name=command value="kodomo_ranking">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="子供ランキング">
	</form></div>
	</td></tr></table><br>
	$disp_para
	<div align=center><form method="POST" action="$this_script">
	<input type=hidden name=mode value="kosodate">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=checkbox name=para value="on"$checked>
	<input type=submit value="パラメーター">
	</form></div>
<table width="90%" border="0" cellspacing="0" align=center class=yosumi><tr><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td><br></td></tr>
<tr><td>$kokugo</td><td>$suugaku</td><td>$rika</td><td>$syakai</td><td>$eigo</td><td>$ongaku</td><td>$bijutu</td><td>$looks</td><td><br></td></tr>
<tr><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td></tr>
<tr><td>$tairyoku</td><td>$kenkou</td><td>$speed</td><td>$power</td><td>$wanryoku</td><td>$kyakuryoku</td><td>$love</td><td>$unique</td><td>$etti</td></tr></table>
<br><br>
EOM
#kokoend
#持ち物フォーム作成
	$syokuryouattane_flag=0;
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
			if ($syo_taikyuu <=0){next;}
			if ($syo_syubetu ne "食料品" && $syo_syubetu ne "ファーストフード"){next;}
			$syokuryou_form .= "<option value=\"$syo_hinmoku\">$syo_hinmokuを</option>";
			$syokuryouattane_flag=1;
	}
	if ($syokuryouattane_flag==0){$syokuryou_form .="<option value=\"\">食料を持っていません</option>";}

#職業ごとの給料をハッシュに代入
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);
	foreach  (@job_hairetu) {
		&job_sprit($_);
		$job_kihonkyuu {$job_name} = $job_kyuuyo;
	}
	
#子供の表示
	$now_time= time;
	$kodomoiruka_flag=0;
	foreach  (@all_kodomo) {
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/);
		chomp $kod_renraku1;
		if ($kod_oya1 eq $name){$konokonooya = $kod_oya2;}elsif($kod_oya2 eq $name){$konokonooya = $kod_oya1;}else{next;}
#子供の名前が無い場合	
		if ($kod_name eq ""){
	#koko2006/11/28 width=90 を消す
			print <<"EOM";
			<table width="90%" border="0" cellspacing="0" cellpadding="6" align=center class=yosumi>
			<tr bgcolor=#ffffff><td style="font-size:12px;color:ff3300" nowrap>$konokonooyaさんとの間に子供ができましたがまだ出産していません。</td></tr>
			</table><br><br>
EOM
			$kodomoiruka_flag=1;
			next;
		}
	#自立している場合
		if ($kod_yobi8 == 1){
			$kono_nenrei = int (($now_time - $kod_yobi1) / (60*60*24));
			$ima_kasegi = ($job_kihonkyuu {$kod_job} * $kono_nenrei) + ($kod_yobi4 * 10);
	
	#koko2006/11/28 width=90 を消す
			print <<"EOM";
			<table width="90%" border="0" cellspacing="0" cellpadding="6" align=center class=yosumi>
			<tr bgcolor=#ffffff><td style="font-size:12px;color:339933" nowrap>$konokonooyaさんとの子供「$kod_name」さんは自立して「$kod_job」になりました。現在、$kono_nenrei歳、給料：$ima_kasegi円</td></tr>
			</table><br>
EOM
	#kokoend
			$kodomoiruka_flag=1;
			next;
		}

		if($in{'renraku1'} && $in{'kod_num'} eq "$kod_num"){$kod_renraku1 = $in{'renraku1'};}else{$in{'renraku1'} = "";}
		if($in{'renraku2'} && $in{'kod_num'} eq "$kod_num"){$kod_renraku2 = $in{'renraku2'};}else{$in{'renraku2'} = "";}

#子供の名前がある場合
	$kono_nenrei = int (($now_time - $kod_yobi1) / (60*60*24));
	$kod_yobi5 = sprintf ("%.1f",$kod_yobi5);
	$kod_yobi6 = sprintf ("%.1f",$kod_yobi6);
	&check_BMI($kod_yobi5,$kod_yobi6);
	&byou_hiduke($kod_yobi7);
	print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="6" align=center class=yosumi>
	<tr bgcolor=#ffffaa><td colspan=7><span  style="font-size:12px;color:ff3300">$kod_name</span>
	（$kono_nenrei歳）$konokonooyaさんとの子供　<span class="honbun2">最後の子育て：$kod_yobi3</span></td></tr>
	<tr bgcolor=#dddddd><td colspan=7>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="kosodate">
	<input type=hidden name=command value="do_kosodate">
	<input type=hidden name=kod_num value="$kod_num">
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
	</select>
	 <select name=par_suuti>
	<option value="1">1</option>
	<option value="2">2</option>
	<option value="3">3</option>
	<option value="4">4</option>
	<option value="5">5</option>
	<option value="10">10</option>
	<option value="20">20</option>
	<option value="30">30</option>
	<option value="40">40</option>
	<option value="50">50</option>
	<option value="60">60</option>
	<option value="70">70</option>
	<option value="80">80</option>
	<option value="90">90</option>
	<option value="100" selected>100</option>
	<option value="200">200</option>
	<option value="300">300</option>
	<option value="400">400</option>
	<option value="500">500</option>
	<option value="600">600</option>
	<option value="700">700</option>
	<option value="800">800</option>
	<option value="900">900</option>
	<option value="1000">1000</option>
	</select>

<font color="#ff0000"><b>÷$kosodatewaruatai</b></font>　支払い <select name="siharaihouhou">$siharai_houhou<option value="現金">現金</option></select><!-- koko2006/12/02 -->

	　<input type=submit value=" あげる ">
	</form>

	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="kosodate">
	<input type=hidden name=command value="do_kosodate">
	<input type=hidden name=kod_num value="$kod_num">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<select name=syokuryou>
	$syokuryou_form
	</select>
	<input type=submit value=" 与える ">
	</form>
	
<form method="POST" action="$this_script" style="margin-top:0; margin-bottom:0;">
<input type=hidden name=mode value="kosodate">
<input type=hidden name=command value="renraku">
<input type=hidden name=kod_num value="$kod_num">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=id value="$k_id">
<input type=hidden name=town_no maxlength="16" value="$in{'town_no'}">
<input type=text name=renraku1 value="$in{'renraku1'}">$kod_renraku1 を目指してがんばろうね。
<input type=text name=renraku2 maxlength="25" value="$kod_renraku2">$kod_renraku2 これをお願い。
<input type=submit value=" 連絡 ">
</form>

	</td></tr>
	<tr><td><span class="honbun2">総合能\力値：</span>$kod_yobi4</td>
	<td>身長：$kod_yobi5 cm</td>
	<td>体重：$kod_yobi6 kg</td>
	<td>体格指数：$BMI（$taikei）</td>
	<td>最後の食事：$bh_tukihi</td>
	</tr>
	<tr>
	<td>国語：$kod_kokugo</td>
	<td>数学：$kod_suugaku</td>
	<td>理科：$kod_rika</td>
	<td>社会：$kod_syakai</td>
	<td>英語：$kod_eigo</td>
	<td>音楽：$kod_ongaku</td>
	<td>美術：$kod_bijutu</td></tr><tr>
	<td>ルックス：$kod_looks</td>
	<td>体力：$kod_tairyoku</td>
	<td>健康：$kod_kenkou</td>
	<td>スピード：$kod_speed</td>
	<td>パワー：$kod_power</td>
	<td>腕力：$kod_wanryoku</td>
	<td>脚力：$kod_kyakuryoku</td></tr><tr>
	<td>LOVE：$kod_love</td>
	<td>面白さ：$kod_unique</td>
	<td>エッチ：$kod_etti</td>
	<td></td>
	<td></td>
	<td></td>
	</tr></table>
	<br><br>
EOM
			$kodomoiruka_flag=1;
	}		#foreach閉じ
	if ($kodomoiruka_flag==0){print "<div align=center class=honbun4>現在、子供はいません。</div>";}
	&hooter("login_view","街へ戻る");
exit;
}

#子供自立サブルーチン
sub kodomo_ziritu {
			my ($kodziritu_num,$kodziritu_name,$kodziritu_oya1,$kodziritu_oya2,$kodziritu_job,$kodziritu_kokugo,$kodziritu_suugaku,$kodziritu_rika,$kodziritu_syakai,$kodziritu_eigo,$kodziritu_ongaku,$kodziritu_bijutu,$kodziritu_looks,$kodziritu_tairyoku,$kodziritu_kenkou,$kodziritu_speed,$kodziritu_power,$kodziritu_wanryoku,$kodziritu_kyakuryoku,$kodziritu_love,$kodziritu_unique,$kodziritu_etti,$kodziritu_yobi1,$kodziritu_yobi2,$kodziritu_yobi3,$kodziritu_yobi4,$kodziritu_yobi5,$kodziritu_yobi6,$kodziritu_yobi7,$kodziritu_yobi8,$kodziritu_yobi9,$kodziritu_yobi10)=split(/<>/,@_[0]);
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	my $top_koumoku = <SP>;
	my @job_hairetu = <SP>;
	close(SP);
#BMIをチェック
	&check_BMI($kod_yobi5,$kod_yobi6);
#給料の多い順にソート
#	foreach (@job_hairetu){
#			$data=$_;
#			$key=(split(/<>/,$data))[18];		#ソートする要素を選ぶ
#			push @job_hairetu_sort,$data;
#			push @ko_keys,$key;
#	}
#		sub bykeys_up{$ko_keys[$b] <=> $ko_keys[$a];} #koko 注意
#		@job_hairetu_sort=@job_hairetu_sort[ sort bykeys_up 0..$#job_hairetu_sort];

# koko 子供の仕事 変更 2005/07/29
	@ko_keys = map {(split /<>/)[18]} @job_hairetu;
	@job_hairetu_sort = @job_hairetu[sort {$ko_keys[$b] <=> $ko_keys[$a]} 0 .. $#ko_keys];
# kokoend

#条件を満たしている職業を検索
	foreach (@job_hairetu_sort){
		&job_sprit($_);

		if ($job_sex && $kodziritu_yobi10 && $kodomo_seibetu eq 'yes'){if($kodziritu_yobi10 ne "$job_sex"){next;}} #koko2007/11/25

		if($kodziritu_kokugo < $job_kokugo){next;}
		if($kodziritu_suugaku < $job_suugaku){next;}
		if($kodziritu_rika < $job_rika){next;}
		if($kodziritu_syakai < $job_syakai){next;}
		if($kodziritu_eigo < $job_eigo){next;}
		if($kodziritu_ongaku < $job_ongaku){next;}
		if($kodziritu_bijutu < $job_bijutu){next;}
		if($BMI < $job_BMI_min){next;}
		if ($job_BMI_max) { if($BMI > $job_BMI_max){next;}}
		if($kodziritu_looks < $job_looks){next;}
		if($kodziritu_tairyoku < $job_tairyoku){next;}
		if($kodziritu_kenkou < $job_kenkou){next;}
		if($kodziritu_speed < $job_speed){next;}
		if($kodziritu_power < $job_power){next;}
		if($kodziritu_wanryoku < $job_wanryoku){next;}
		if($kodziritu_kyakuryoku < $job_kyakuryoku){next;}
		if($kodziritu_love < $job_love){next;}
		if($kodziritu_unique < $job_unique){next;}
		if($kodziritu_etti < $job_etti){next;}
		if($kodziritu_yobi5 < $job_sintyou){next;}
		last;
	}	#foreach閉じ
		if ($job_name eq ""){$job_name = "浮浪者";}
		$return_job = $job_name;
	&lock;
		&news_kiroku("就職","$kodziritu_oya1さんと$kodziritu_oya2さんの子供「$kod_name」さんが自立して$job_nameになりました。");
	&unlock;
}

#離婚時の配偶者ID削除処理
sub kekkon_id_sakujo {
#koko2007/05/28
#	if ($house_type){

	&id_check($_[0]);
	&openAitelog ($return_id);
	if ($aite_house_type eq ""){return;}
	$jibun_house_type = $aite_house_type; #koko2007/05/28
	$aite_house_type = "";
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);

	&openAitelog ($jibun_house_type);
	$aite_house_type = "";
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);

	&news_kiroku("別れ","$cn_name1さんと$cn_name2さんが別れました。");

#	}
#kokoend
}
############# 別れ確認 ############### koko2008/01/15
sub wakare{
	&header;
	print <<"EOM";
	<div align=center><br>
<table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
本当に別れますか。？
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="wakare_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=id value="$in{'k_id'}">
	<input type=hidden name=town_no value=$in{'town_no'}>
	<input type=hidden name=sousinsaki_name value="$in{'sousinsaki_name'}">
	<input type="submit" value=" 分かれる ">
	</form>
</td></tr></table><br>
	</div>
EOM
	&hooter("login_view","街へ戻る");
	exit;
}

############## 別れの処理 ############ koko2007/11/23
sub wakare_do{
	open(COA,"< $couple_file") || &error("$couple_fileに書き込めません");
	eval{ flock (COA, 1); };
	@all_couple = <COA>;
	close(COA);

	foreach (@all_couple){
		($cn_number,$cn_name1,$cn_name2,$cn_joutai,$cn_total_aijou,$cn_omoide1,$cn_omoide2,$cn_omoide3,$cn_omoide4,$cn_omoide5,$cn_kodomo,$cn_yobi1,$cn_yobi2,$cn_yobi3,$cn_yobi4,$cn_yobi5)= split(/<>/);
		if ($in{'sousinsaki_name'} eq $cn_name1 || $in{'sousinsaki_name'} eq $cn_name2 and $in{'name'} eq $cn_name1 || $in{'name'} eq $cn_name2){
			&message_only("$cn_name1さんと$cn_name2さんが別れました。");
			&news_kiroku("別れ","$cn_name1さんと$cn_name2さんが別れました。");
			$wakare1 = $cn_name1;
			$cn_joutai_hoji = $cn_joutai; #koko2008/01/13
			$cn_name1_hoji = $cn_name1; #koko2008/01/13
			$cn_name2_hoji = $cn_name2; #koko2008/01/13
			&hooter("login_view","戻る");
			next;
		}
		$couple_tmp = "$cn_number<>$cn_name1<>$cn_name2<>$cn_joutai<>$cn_total_aijou<>$cn_omoide1<>$cn_omoide2<>$cn_omoide3<>$cn_omoide4<>$cn_omoide5<>$cn_kodomo<>$cn_yobi1<>$cn_yobi2<>$cn_yobi3<>$cn_yobi4<>$cn_yobi5<>\n";
		push (@new_all_couple,$couple_tmp);
	}
	open(COP,">$couple_file") || &error("$couple_fileに書き込めません");
	eval{ flock (COP, 2); };
	print COP @new_all_couple;
	close(COP);

	if($cn_joutai_hoji eq "配偶者" && ($in{'sousinsaki_name'} eq $cn_name1_hoji || $in{'sousinsaki_name'} eq $cn_name2_hoji) && ($in{'name'} eq $cn_name1_hoji || $in{'name'} eq $cn_name2_hoji) ){ #2008/01/04,01/13
		&id_check($cn_name1_hoji); #koko2008/01/13
		&openAitelog ($return_id);
		$jibun_house_type = "";
		$aite_house_type = "";
		&aite_temp_routin;
		open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
		eval{ flock (OUT, 2); };
		print OUT $aite_k_temp;
		close(OUT);
		&id_check($cn_name2_hoji); #koko2008/01/13
		&openAitelog ($return_id);
		$jibun_house_type = "";
		$aite_house_type = "";
		&aite_temp_routin;
		open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
		eval{ flock (OUT, 2); };
		print OUT $aite_k_temp;
		close(OUT);
	}

# 子供のチェック
	open(KOD,"< $kodomo_file") || &error("Open Error : $kodomo_file");
	eval{ flock (KOD, 1); };
	@all_kodomo=<KOD>;
	close(KOD);
	@new_all_kodomo = ();
	$kodomoatta_flg = 0;
	$umu_news = "0";
	foreach $kodomo_tmp(@all_kodomo){
		($kod_num,$kod_name,$kod_oya1,$kod_oya2,$kod_job,$kod_kokugo,$kod_suugaku,$kod_rika,$kod_syakai,$kod_eigo,$kod_ongaku,$kod_bijutu,$kod_looks,$kod_tairyoku,$kod_kenkou,$kod_speed,$kod_power,$kod_wanryoku,$kod_kyakuryoku,$kod_love,$kod_unique,$kod_etti,$kod_yobi1,$kod_yobi2,$kod_yobi3,$kod_yobi4,$kod_yobi5,$kod_yobi6,$kod_yobi7,$kod_yobi8,$kod_yobi9,$kod_yobi10,$kod_renraku1,$kod_renraku2)=split(/<>/,$kodomo_tmp);
		chomp $kod_renraku1;
		if(($in{'sousinsaki_name'} eq $kod_oya1 || $in{'sousinsaki_name'} eq $kod_oya2) && ($in{'name'} eq $kod_oya1 || $in{'name'} eq $kod_oya2)){ #2008/01/05
			next;
		}
		push (@new_all_kodomo,$kodomo_tmp);
	}
	&lock; # 送金先が無くなるのでそのカップルの子は居なくなります。
	open(KODO,">$kodomo_file") || &error("$kodomo_fileに書き込めません");
	eval{ flock (KODO, 2); };
	print KODO @new_all_kodomo;
	close(KODO);
	&unlock;
}

#ギフト送付処理 追加処理　koko2007/12/20
sub gift_souhu_syori2 {
#自分の持ち物リストから商品を消去
	if(!$k_id){&error("mono.cgi エラー command7")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$monoatta_flag = 0;
	@new_myitem_hairetu =();#koko2007/06/05
	foreach $myitem (@myitem_hairetu){
		&syouhin_sprit($myitem);
#koko2007/07/23 クーポン 2007/08/04
		if ($syo_hinmoku eq "$in{'gift_souhu'}" && $syo_syubetu eq "ギフト" && $monoatta_flag == 0 && $in{'gift_souhu'} ne "クーポン"){
			$ageru_gift_copy = $myitem; 
			$monoatta_flag = 1;
			next;
		} #koko2006/10/20
		if ($syo_hinmoku eq "クーポン" && $in{'gift_souhu'} eq "クーポン"){
			$syo_taikyuu--; #koko2007/08/04
			$ageru_gift_copy = $myitem;
			$monoatta_flag = 1;
			if ($syo_taikyuu <= 0){
				next;
			}
		}
#end  クーポン
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}
	if ($monoatta_flag == 0){&error("既に商品はありません。");}
#購入日を記録、単価は0円、種別をギフト商品にする
	&syouhin_sprit($ageru_gift_copy);
	$syo_kounyuubi = time;
	$tanka = 0;

	if ($syo_hinmoku ne "クーポン"){
		$syo_syubetu = "ギフト商品";
	}else{
		$syo_syubetu = "ギフト商品";
	}
	#koko2006/10/09
	$syo_kouka =~ s/,ギフト//g;
	$syo_kouka =~ s/ギフト//g;
	($syo_comment) = split(/\t/,$syo_comment);
	$syo_comment .= "\t$nameさんからの贈り物です。";
	#kokoend
	if ($syo_hinmoku eq "クーポン"){
		$syo_taikyuu = 1;
	}
	&syouhin_temp;
	$okuraretamono = $syo_temp;
#相手の持ち物リストに商品を追加
	if(!$return_id){&error("IDが見つかりません。command8");} #koko2007/10/13
	$aite_monokiroku_file="./member/$return_id/mono.cgi";
	open(ASP,"< $aite_monokiroku_file") || &error("Open Error : $aite_monokiroku_file");
	eval{ flock (ASP, 1); };
	@aite_item_hairetu = <ASP>;
	close(ASP);
#koko2007/07/23 クーポン
	@new_aite_item_hairetu = ();
	$kupon_okuri = 0;
	foreach (@aite_item_hairetu){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "ギフト" && $syo_hinmoku eq "クーポン" && $in{'gift_souhu'} eq "クーポン"){
			$kupon_okuri = 1;
			$syo_taikyuu++;
		}elsif ($syo_syubetu eq "ギフト商品"){
			$gift_count ++;
		}
		&syouhin_temp;
		push @new_aite_item_hairetu,$syo_temp;
	}
	
	if ($kupon_okuri == 1){
		@aite_item_hairetu = (@new_aite_item_hairetu);

	}elsif ($gift_count >= $gift_gendo){&error("お相手の方のギフトが限度数の$gift_gendoを超えるため送付できません");
	}else{
		push (@new_aite_item_hairetu,$okuraretamono);
		@aite_item_hairetu = (@new_aite_item_hairetu);
	}
#end クーポン
#相手の所有物ファイルを更新
	&lock;
	open(ASP,">$aite_monokiroku_file") || &error("Write Error : $aite_monokiroku_file");
	eval{ flock (ASP, 2); };
	print ASP @aite_item_hairetu;
	close(ASP);	
#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);
#koko2006/11/27　2007/09/02
	if (-z $monokiroku_file){
		$loop_count = 0;
		while ($loop_count <= 10){
			for (0..50){$i=0;}
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
	}
#kokoend
	&unlock;
}




