#!/usr/bin/perl

################################
# 番号の数
$loto_n = 36;
# 一口購入金額
$koniyukingaku = 2500;
#抽選時間
$koushinjikan = 6;
#保存限界抽選
$saidaisanka = 200;
# 1人の購入上限 (0または""で規制無し
$hitri_konu_zyougen = 20;
# ロトの購入ファイル名
$lotokonuu_f = "./log_dir/loto_konuu6.cgi";
#抽選ログファイル
$lotokekka_f = "./log_dir/loto_kekka6.cgi";
#賞金7->1当
@syokin_hairetu = (0,2500,5000,100000,1000000,10000000,100000000);
# ボタンでの名前を書くか('yes'or'no')
$on_botan = 'yes';
################################

$this_script = 'loto6.cgi';
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

	if(!$k_id){&error("k_id が存在しません。入り直してください。");} #2008/01/06
	if($in{'mode'} eq "loto_game"){&loto_game;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;


sub loto_game {
	if ($hitri_konu_zyougen){
		$disp_zyougen = "お一人様の購入上限は$hitri_konu_zyougen口です。\n";
	}
	open(MA,"< $lotokonuu_f") || &error("$lotokonuu_fが開けません");
	eval{ flock (MA, 1); };
	$loto_kanri = <MA>;
	@loto_konuu_data = <MA>;
	close(MA);

	($higawri,$koushin,$hinichi) = split(/<>/,$loto_kanri);

	($sec,$min,$hour,$mday,$mon,$year) = localtime(time);
	$mon++;
	$year += 1900;

	if (($koushin > $hour && $higawri == 1) || $hinichi ne $mday){
		
		$higawri = 0;
		$koushin = $hour;
		$hinichi = $mday;
		$loto_kanri = "$higawri<>$koushin<>$hinichi<>\n";
		&lock;
		open(KB,">$lotokonuu_f")|| &error("Open Error : $lotokonuu_f");
		eval{ flock (KB, 2); };
		print KB $loto_kanri;
		print KB @loto_konuu_data;
		close(KB);
		&unlock;
	}
	if($hour >= $koushinjikan && $higawri == 0 || $#loto_konuu_data +1 >= $saidaisanka){
		$higawri = 1;
		$koushin = $hour;
#抽選開始
		@loto_tusen = &randcheck($loto_n,6);
		$tousenbangou = "$loto_tusen[0],$loto_tusen[1],$loto_tusen[2],$loto_tusen[3],$loto_tusen[4],$loto_tusen[5]";
		$loto_kanri1 = "$higawri<>$koushin<>$hinichi<>$loto_tusen[0]<>$loto_tusen[1]<>$loto_tusen[2]<>$loto_tusen[3]<>$loto_tusen[4]<>$loto_tusen[5]<>\n";

		$loop_i = 0;
		foreach (@loto_konuu_data){
			($loto_name,$loto_id,$loto0,$loto1,$loto2,$loto3,$loto4,$loto5,$loto_time,$loto_atari) = split(/<>/);
			if ($genzainame eq ""){
				$genzainame = $loto_name;
				$sougou_syokin = 0;
			}
			if ($genzainame eq $loto_name){
				$atari = 0;
				$i = 0;
				for (0 .. 5){
					if ($loto0 == $loto_tusen[$i]){
						$loto0 = "<font color=\"#0000ff\"><b>$loto0</b></font>";	
						$atari++;
						last;
					}
					$i++;
				}
				$i = 0;
				for (0 .. 5){
					if ($loto1 == $loto_tusen[$i]){
						$loto1 = "<font color=\"#0000ff\"><b>$loto1</b></font>";
						$atari++;
						last;
					}
					$i++;
				}
				$i = 0;
				for (0 .. 5){
					if ($loto2 == $loto_tusen[$i]){
						$loto2 = "<font color=\"#0000ff\"><b>$loto2</b></font>";
						$atari++;
						last;
					}
					$i++;
				}
				$i = 0;
				for (0 .. 5){
					if ($loto3 == $loto_tusen[$i]){
						$loto3 = "<font color=\"#0000ff\"><b>$loto3</b></font>";
						$atari++;
						last;
					}
					$i++;
				}
				$i = 0;
				for (0 .. 5){
					if ($loto4 == $loto_tusen[$i]){
						$loto4 = "<font color=\"#0000ff\"><b>$loto4</b></font>";
						$atari++;
						last;
					}
					$i++;
				}
				$i = 0;
				for (0 .. 5){
					if ($loto5 == $loto_tusen[$i]){
						$loto5 = "<font color=\"#0000ff\"><b>$loto5</b></font>";
						$atari++;
						last;
					}
					$i++;
				}
				$loto_atari = $syokin_hairetu[$atari];
				$loto_syo = 7 - $atari;
				$sougou_syokin += $loto_atari;
				$tyusen_cado = "$loto_name<>$loto_id<>$loto0<>$loto1<>$loto2<>$loto3<>$loto4<>$loto5<>$loto_time<>$loto_atari<>$loto_syo<>$sougou_syokin<>\n";
				push @loto_sumi,$tyusen_cado;
				$loop_i++;
				($loto_name1,$loto_id1) = split(/<>/,$loto_konuu_data[$loop_i]);

#print "($loto_name,$loto_id)($loto_name1,$loto_id1)";

				if ($loto_name ne $loto_name1){ # 次が別口
#koko2006/12/22				#送金
					$genzainame = "";

					if (not(-e "./member/$loto_id/log.cgi")){&err_next("member/$loto_id/log.cgiがありません。");}
					if (-z "./member/$loto_id/log.cgi"){&err_next("member/$loto_id/log.cgiが異常です。");}
					if (not(-e "./member/$loto_id/ginkoumeisai.cgi")){&err_next("member/$loto_id/ginkoumeisai.cgiがありません。");}
					
					&lock;	
					&openAitelog_in ($loto_id);

					$aite_bank += $sougou_syokin;
	
					&aite_temp_routin;
					open(OUT,">$aite_log_file") || &err_next("$aite_log_fileが開けません");
					eval{ flock (OUT, 2); };
					print OUT $aite_k_temp;
					close(OUT);

							 #("明細",出金額,入金額,残高,普or定,振込先ID,"lock_off or 無し")
					&aite_kityou_syori_in("ロトの当たり金","",$sougou_syokin,$aite_bank,"普",$loto_id,"lock_off");
					&unlock;
					#送金終了


				} # 購入者の終わり
			} #　$genzainame eq $loto_name終了
		} # foreach (@loto_konuu_data)終了
#######内部エラー処理
sub err_next {
	push @loto_sumi,"$loto_name<>$loto_id<><><><><><><><><><>$_[0]<>\n";
	next;
}
######相手の方のログファイル
sub openAitelog_in {
	$aite_log_file = "./member/@_[0]/log.cgi";
	open(AIT,"< $aite_log_file") || &err_next("お相手の方のログファイル（$aite_log_file）が開けません。");
	eval{ flock (AIT, 1); };
	$aite_prof = <AIT>;
	if($aite_prof == ""){&err_next("@_[0]/log.cgi お相手の方のログファイルに問題があります。");} #koko2006/12/22
	&aite_sprit($aite_prof);
	close(AIT);
}
#######相手の記帳処理
sub aite_kityou_syori_in {
	my (@aite_tuutyou);
	if (@_[6] ne "lock_off"){
		&lock;
	}
	$ginkoumeisai_file="./member/@_[5]/ginkoumeisai.cgi";
	open(GM,"< $ginkoumeisai_file") || &err_next("相手の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@aite_tuutyou = <GM>;
	close(GM);
	&time_get;
	$torihikinaiyou = "$date<>@_[0]<>@_[1]<>@_[2]<>@_[3]<>@_[4]<>\n";
#("明細",出金額,入金額,残高,普or定,振込先ID,"lock_off or 無し")
	unshift (@aite_tuutyou,$torihikinaiyou);
	$meisai_kensuu = @aite_tuutyou;
	if ($meisai_kensuu > 100){pop (@aite_tuutyou);}
	open(GMO,">$ginkoumeisai_file") || &err_next("相手の預金通帳ファイルに書き込めません");
	eval{ flock (GMO, 2); };
	print GMO @aite_tuutyou;
	close(GMO);
	if (@_[6] ne "lock_off"){
		&unlock;
	}
}
###########################
#kokoend
		&lock;
		open(KB,">$lotokekka_f")|| &error("Open Error : $lotokonuu_f");
		eval{ flock (KB, 2); };
		print KB $loto_kanri1;
		print KB @loto_sumi;
		close(KB);

		@loto_all = ();
		@loto_konuu_data = ();
		$loto_kanri = "$higawri<>$koushin<>$hinichi<>\n";
		open(KB,">$lotokonuu_f")|| &error("Open Error : $lotokonuu_f");
		eval{ flock (KB, 2); };
		print KB $loto_kanri;
		print KB @loto_all;
		close(KB);
		&unlock;

	} # 抽選終了
# 購入
	$maisu = 0;
	foreach (@loto_konuu_data){
		($loto_name,$loto_id,$loto0,$loto1,$loto2,$loto3,$loto4,$loto5,$loto_time,$loto_atari) = split(/<>/);
		if ($loto_name eq $in{'name'}){
			$maisu++;
			if ($hitri_konu_zyougen){
				if ($hitri_konu_zyougen <= $maisu ){
					$mesege = "お一人様の購入上限は$hitri_konu_zyougen口です。\n";
				}
			}
			push @loto_my,$_;
			next;
		}
		push @lotomemba,$_;
	}
	if (!$mesege){ #購入限度になっていない時
		if ($in{'randamu_set'}){
			@loto = &randcheck($loto_n,6);
			$loto0 = $loto[0];
			$loto1 = $loto[1];
			$loto2 = $loto[2];
			$loto3 = $loto[3];
			$loto4 = $loto[4];
			$loto5 = $loto[5];

			$konyu_masegi = "[$loto0,$loto1,$loto2,$loto3,$loto4,$loto5]";
		
		}elsif(@loto){
			(@loto) = split(/,/, $loto[0]);
			shift(@loto);
			if ($#loto != 5){&error("６個数字を選んでください。");}

#			@loto = sort{$a <=> $b} @loto;
			$loto0 = $loto[0];
			$loto1 = $loto[1];
			$loto2 = $loto[2];
			$loto3 = $loto[3];
			$loto4 = $loto[4];
			$loto5 = $loto[5];

			$konyu_masegi = "[$loto0,$loto1,$loto2,$loto3,$loto4,$loto5]";
		}else{
			$konyu_masegi = "";
		}

		if ($konyu_masegi ne ""){
			$money -= $koniyukingaku;

			&temp_routin;
			&log_kousin($my_log_file,$k_temp);

			$loto_atari = "";

			$loto_time = time;
#koko2006/12/13
			$loto0 =~ s/[^0-9]//g;
			$loto1 =~ s/[^0-9]//g;
			$loto2 =~ s/[^0-9]//g;
			$loto3 =~ s/[^0-9]//g;
			$loto4 =~ s/[^0-9]//g;
			$loto5 =~ s/[^0-9]//g;
#kokoend
			$new_cado = "$in{'name'}<>$in{'k_id'}<>$loto0<>$loto1<>$loto2<>$loto3<>$loto4<>$loto5<>$loto_time<>$loto_atari<>\n";
			push @loto_my,$new_cado;
			@loto_all = (@loto_my,@lotomemba);

			&lock;
			open(KB,">$lotokonuu_f")|| &error("Open Error : $lotokonuu_f");
			eval{ flock (KB, 2); };
			print KB $loto_kanri;
			print KB @loto_all;
			close(KB);
			&unlock;
		}
		if (!@loto_all){@loto_all = @loto_konuu_data;}
		$mesege = "<input type=submit value=\"買います\">\n";
	}else{
		@loto_all = (@loto_my,@lotomemba);
	}

	&header(ginkou_style);
	print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="80%">
<tr><td>
<div class=midasi align=center>++ LOTO6ゲーム ++</div><div align=center>
<table border="0" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="460">
<tr><td>
<form method=\"POST\" action="$this_script">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="loto_game">
<input type=hidden name=command value="hiku">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
EOM

	$loop = 1;
	while ($loop <= $loto_n) {
		if ($loop < 10){
			$tmp = "0$loop";
		}else{$tmp = $loop;}
		print "<input type=\"checkbox\" name=\"loto\" value=\",$tmp\">$tmp ";
		$loop++;
	}
	print <<"EOM";
</td></tr><tr><td align="center">
<input type="checkbox" name="randamu_set" value="yes" checked> ランダムチェック 
$mesege
 ６個のチェックです。<br>$konyu_masegi</form>
</td></tr><tr><td>一口$koniyukingaku円です。$disp_zyougen<br>当選金は銀行の普通口座に振り込まれます。
</td></tr></table>
<tr><td>
</td></tr></table>
EOM

	print <<"EOM";
<table border="1" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="80%">
<tr><td>
<table border="0" bgcolor="#ffffff" cellspacing="0" cellpadding="0" align="center" width="560">
<tr><td colspan="4">購入状況</td></tr>
EOM
	$i=0;
	foreach (@loto_all){
		($loto_name,$loto_id,$loto0,$loto1,$loto2,$loto3,$loto4,$loto5,$loto_time,$loto_syokin) = split(/<>/);
		if($loto_name ne $meno_name){
			$meno_name = $loto_name;
			if ($i %  4 == 1){
				print "<td></td><td></td><td></td></tr>\n";
				$i += 3;
			}
			if ($i %  4 == 2){
				print "<td></td><td></td></tr>\n";
				$i += 2;
			}
			if ($i %  4 == 3){
				print "<td></td></tr>\n";
				$i += 1;
			}
#koko2006/12/13
			if (not(-e "./member/$loto_id/oriie_settei.cgi")){$loto_id = "";}
			if ($loto_id ne ""){
				open(IN,"< ./member/$loto_id/oriie_settei.cgi") || &error("Open Error : /member/$loto_id/oriie_settei.cgi");
				eval{ flock (IN, 1); };
				$ie_dat = <IN>;
				close(IN);
				(@ie_hairet) = split(/<>/, $ie_dat);
				if (!($ie_hairet[0] eq "1" || $ie_hairet[1] eq "1" || $ie_hairet[2] eq "1" || $ie_hairet[3] eq "1")){ $loto_id = "";}
			}

			if ($loto_id ne "" && $on_botan eq 'yes'){

	print <<"EOM"; #2006/12/16
<tr><td colspan=\"4\">
<form method=POST action="original_house.cgi" style="margin-top: 0em;margin-bottom: 0em">
<input type=hidden name=gamerand value="$in{'gamerand'}">
<input type=hidden name=mode value="houmon">
<input type=hidden name=ori_ie_id value="$loto_id">
<input type=hidden name=name value="$name">
<input type=hidden name=pass value="$pass">
<input type=hidden name=k_id value="$in{'k_id'}"><!-- koko2006/12/13 -->
<input type=hidden name=con_sele value="1">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="$loto_nameさん">
</form>
</td></tr><tr>
EOM
			}else{
				print "<tr><td colspan=\"4\"><b>$loto_nameさん</b></td></tr><tr>\n";
			}
#kokoend
			$i =1;
		}
		print "<td>[$loto0,$loto1,$loto2,$loto3,$loto4,$loto5]</td>\n";
		if ($i %  4== 0){print "</tr><tr>\n";}
		$i++;
	}
	print "</tr></table>\n";

# 前回の結果
	open(MA,"< $lotokekka_f") || &error("$lotokekka_fが開けません");
	eval{ flock (MA, 1); };
	$loto_kanri1 = <MA>;
	@loto_sumi = <MA>;
	close(MA);

	print "<br><table border=\"0\" bgcolor=\"#ffffff\" cellspacing=\"0\" cellpadding=\"0\" align=\"center\" width=\"560\">\n";

	($higawri,$koushin,$hinichi,$loto_tusen0,$loto_tusen1,$loto_tusen2,$loto_tusen3,$loto_tusen4,$loto_tusen5) = split(/<>/,$loto_kanri1);

	print "<tr><td colspan=\"2\"><b>前回の結果</b>　　[<font color=\"#0000ff\"><b> $loto_tusen0,$loto_tusen1,$loto_tusen2,$loto_tusen3,$loto_tusen4,$loto_tusen5 </b></font>]</td></tr>\n";
	$i=0;
	foreach (@loto_sumi){
		($loto_name1,$loto_id,$loto0,$loto1,$loto2,$loto3,$loto4,$loto5,$loto_time,$loto_atari,$loto_syo,$sougou_syokin) = split(/<>/);
		if($loto_name1 ne $maeno_name){
			$maeno_name = $loto_name1;

			if ($i %  1== 1){
				print "<td></td></tr>\n";
				$i += 1;
			}
			print "<tr><td colspan=\"2\">$loto_name1さん</td></tr><tr>\n";
			$i = 1;
		}
#koko2006/12/22
		if (!$loto0 && !$loto1 && !$loto2 && !$loto3 && !$loto4 && !$loto5){
			print "<td><font color=\"#ff0000\">【$sougou_syokin】</font></td>\n";
		}else{
			print "<td><font color=\"#ff00ff\">【</font>[$loto0,$loto1,$loto2,$loto3,$loto4,$loto5] $loto_syo当 $loto_atari <font color=\"#ff00ff\">$sougou_syokin円】</font></td>\n";
		}
#kokoend
		if ($i %  2== 0){print "</tr><tr>\n";}
		$i++;
	}
	print "</tr></table>\n";

	print "</td></tr></table>\n";

	print "<div align=\"right\">Edit:たっちゃん<div>\n";

	&hooter("login_view","戻る");
	exit;
}		#sub閉じ

##### くじ引き　01 以上 $_[0] 以下の数字を $_[1] 個選び返す
sub randcheck {
	my @list = ();
	my $str = "";
	my $i = 0;
	while ($i < $_[1]) {
		my $tmp = sprintf("%02d",(rand($_[0]))+1);
		if (index($str, $tmp) < 0) {
			$str .= ",$tmp";
			$i++;
		}
	}
	@list = split /,/,$str;
	shift(@list);	# 先頭の空要素取り除き
	@list = sort{$a <=> $b} @list;
	return (@list);
}

__END__


