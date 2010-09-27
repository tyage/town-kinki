#!/usr/bin/perl

# ↑お使いのサーバーのパスに合わせてください。
################################
# unit.pl
#"競売" => "<form method=POST action=\"auction.cgi\"><input type=hidden name=mode value=\"auction\"><input type=hidden name=name value=\"$name\"><input type=hidden name=pass value=\"$pass\"><input type=hidden name=k_id value=\"$k_id\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><td height=32 width=32><input type=image src='$img_dir/gouseiyai.gif'  onMouseOver='onMes5(\"競売所です。\")' onMouseOut='onMes5(\"\")'></td></form>\n",
################################

# ログファイル
$auction_log = './log_dir/auction_log.cgi';

# 設定無しの時の最低上げ幅。
$syokiagehaba = 10;

# 上限価格
$auc_jyougen = '';

# オークションの数
$max_auc = 20;
#出品者<>出品者ID<>競売者<>競売者ID<>即決価格<>始め値<>上げ幅<>現在値<>登録時間<>締め切り時間<>落札時間<>落札価格<>終了<>商種別<>商品<>コメント出品者<>コメント競売者<>

$this_script = 'auction.cgi';
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

	$in{'com_syupin'} =~ s/</&lt;/g; #koko2008/03/26
	$in{'com_syupin'} =~ s/>/&gt;/g; #koko2008/03/26
	$in{'com_sanka'} =~ s/</&lt;/g; #koko2008/03/26
	$in{'com_sanka'} =~ s/>/&gt;/g; #koko2008/03/26

	if(!$k_id){&error("k_id が存在しません。入り直してください。");} #koko2008/01/06

	if($in{'mode'} eq "auction"){&auction;}
	if($in{'mode'} eq "syupin"){&syupin;}
	if($in{'mode'} eq "syupin_do"){&syupin_do;}

	else{&error("「戻る」ボタンで街に戻ってください");}
exit;

sub auction{
	open(IN,"< $auction_log") || &error("Open Error : $auction_log");
	eval{ flock (IN, 1); };
	@auction_dat = <IN>;
	close(IN);


	@auc_Keys = map {(split /<>/)[9]} @auction_dat;
	@auction_dat = @auction_dat[sort {@auc_Keys[$b] <=> @auc_Keys[$a]} 0 .. $#auc_Keys]; #koko2008/03/19

	foreach (@auction_dat){
		($auc_dat,$syo_dat) = split(/\t\t/);
		($auc_name,$auc_id,$auc_t_name,$auc_t_id,$auc_soku,$auc_strat,$auk_haba,$auc_ima,$auc_e_tim,$auc_end_t,$auc_rak_tim,$auc_rak_kakaku,$auc_end,$euc_s_subetu,$euc_s_syohin,$com_syupin,$com_sanka) = split(/<>/,$auc_dat);
		if(!$auc_end){$aru++;}
	}

	if($aru <= $max_auc - 5){
		$disp_in = <<"EOM";
	<form method="POST" action="$this_script">
<input type=hidden name=mode value="syupin">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="出品へ">
</form>
EOM
	}


	&header(gym_style);
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>●ルール説明<br>締め切り時間前1分間ＵＰが無ければ、落札決定します。<br>
【注意】最低上げ幅より端数が出た場合は切り上げとなります。
<td  bgcolor=#ff33ff align=center width=35%><h1>オークション</h1></td>
</tr></table><br>
<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
<tr><td>
$disp_in
EOM
	$ima_time = time();

	$i = 0;
	foreach (@auction_dat){
		($auc_dat,$syo_dat) = split(/\t\t/);
		($auc_name,$auc_id,$auc_t_name,$auc_t_id,$auc_soku,$auc_strat,$auk_haba,$auc_ima,$auc_e_tim,$auc_end_t,$auc_rak_tim,$auc_rak_kakaku,$auc_end,$euc_s_subetu,$euc_s_syohin,$com_syupin,$com_sanka) = split(/<>/,$auc_dat);
		&syouhin_sprit($syo_dat);

		if(!$syo_taikyuu){next;} #2008/03/15
		if(!$auc_t_name && $auc_end_t <= $ima_time && !$auc_end){ #投票無しkoko2008/03/20
			
			if(!$auc_id){&error("mono.cgi エラー auction1")} #koko2007/11/18
			if(open(AUC,"< ./member/$auc_id/mono.cgi")){
				eval{ flock (AUC, 1); };
				@myitem_hairetu = <AUC>;
				close(AUC);
			}else{
				next;
			}

			push @myitem_hairetu,$syo_dat;

			if(!$auc_id){&error("mono.cgi エラー auction2")} #koko2007/11/18
			open(AUC,">./member/$auc_id/mono.cgi") || &error("Open Error : $monokiroku_file");
			eval{ flock (AUC, 2); };
			print AUC @myitem_hairetu;
			close(AUC);

			&openAitelog ($auc_id);
			&aite_temp_routin;
			open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
			eval{ flock (OUT, 2); };
			print OUT $aite_k_temp;
			close(OUT);
			&aite_kityou_syori("$euc_s_syohinの落札はありませんでした。",0,0,$aite_bank,"普",$auc_id,"lock_off");

			$auc_rak_tim = $auc_end_t;
			$auc_rak_kakaku = $auc_ima;
			$auc_end =1;
			$syo_kounyuubi = $ima_time;
			&syouhin_temp($syo_dat);
			$auc_dat_up = "$auc_name<>$auc_id<>$auc_t_name<>$auc_t_id<>$auc_soku<>$auc_strat<>$auk_haba<>$auc_ima<>$auc_e_tim<>$auc_end_t<>$auc_rak_tim<>$auc_rak_kakaku<>$auc_end<>$euc_s_subetu<>$euc_s_syohin<>$com_syupin<>$com_sanka<>\t\t$syo_temp";

			$auction_dat[$i] = $auc_dat_up;#2007/11/02
			$dat_chiengi = 1;
		}

		if($auc_t_name && $auc_end_t <= $ima_time && !$auc_end){ #競争落札koko2008/03/20
			if(!$auc_end_t){$auc_end_t = $ima_time;}#koko2008/03/20
			$auc_rak_tim = $auc_end_t;
			$auc_rak_kakaku = $auc_ima;
		
			$auc_end = 1;
			if($euc_s_subetu eq 'ギフト' && $euc_s_syohin eq 'クーポン'){
				$auc_taikyuu = $syo_taikyuu;
			}else{
				$auc_taikyuu = '';
			}
			&ukewatashi;
		}

		if($auc_end){
			push @auc_end_syo,$_; #koko2008/03/19
			$i++;
			next;
		}

		if($in{'up'} && $i == $in{'no'}){
			if($auc_name eq $in{'name'}){$auc_err = 1;&error("出品者は参加できません。");}   #test #付ける
			if($auc_t_name eq $in{'name'}){$auc_err = 1;&error("連続アップは禁止します。");} #test #付ける
			if(!$auk_haba){$auk_haba = $syokiagehaba;}
			$puraisu_up = int(($auc_ima + $auk_haba) / $auk_haba) * $auk_haba;
			if($in{'touhyou'} =~ m/\D/){&error("数値以外は受け付けられません。");}
			$k_sousisan = $money + $bank + $super_teiki - ($loan_nitigaku * $loan_kaisuu);
			
			if($auc_soku*2 < $in{'touhyou'} and $auc_soku){&error("投票は即決価格の二倍以下とさせていただきます。");}#チャゲ改造
			if($in{'touhyou'} > $k_sousisan){&error("総資産以上の買い物は出来ません。");}
			if($auc_jyougen && $in{'touhyou'} > $auc_jyougen){$in{'touhyou'} = $auc_jyougen;}
			$com_sanka = $in{'com_sanka'};
			if($puraisu_up <= $in{'touhyou'}){
				$auc_ima = $in{'touhyou'};

				if($auc_end_t - 180 > $ima_time && $auc_soku && $auc_soku <= $in{'touhyou'}){ # 即決
					$auc_ima = $in{'touhyou'};
					$auc_end = 1;
					$auc_t_name = $in{'name'};
					$auc_t_id = $in{'k_id'};
					$auc_ima = $in{'touhyou'};
					$auc_rak_tim = $ima_time;
					$auc_rak_kakaku = $auc_ima;
					$auc_end_t = $ima_time; #koko2007/10/29
					$syo_kounyuubi = $ima_time;
					&syouhin_temp($syo_dat);
					$auc_dat_up = "$auc_name<>$auc_id<>$auc_t_name<>$auc_t_id<>$auc_soku<>$auc_strat<>$auk_haba<>$auc_ima<>$auc_e_tim<>$auc_end_t<>$auc_rak_tim<>$auc_rak_kakaku<>$auc_end<>$euc_s_subetu<>$euc_s_syohin<>$com_syupin<>$in{'com_sanka'}<>\t\t$syo_temp";

					$auction_dat[$i] = $auc_dat_up;#2007/11/02
#2007/11/02
					if($euc_s_subetu eq 'ギフト' && $euc_s_syohin eq 'クーポン'){
						$auc_taikyuu = $syo_taikyuu;
					}else{
						$auc_taikyuu = '';
					}
#end2007/11/02
					&ukewatashi;
					push @auc_end_syo,$_; #koko2008/03/19
					$i++;
					next;
				}
				if($auc_end_t-60 < $ima_time && $auc_end_t > $ima_time){$auc_end_t = $ima_time + 60;}
				$auc_ima = $in{'touhyou'};
				$auc_t_name = $in{'name'};
				$auc_t_id = $in{'k_id'};

				$auc_dat_up = "$auc_name<>$auc_id<>$auc_t_name<>$auc_t_id<>$auc_soku<>$auc_strat<>$auk_haba<>$auc_ima<>$auc_e_tim<>$auc_end_t<>$auc_rak_tim<>$auc_rak_kakaku<>$auc_end<>$euc_s_subetu<>$euc_s_syohin<>$com_syupin<>$in{'com_sanka'}<>\t\t$syo_dat";
				$auction_dat[$i] = $auc_dat_up;#2007/11/02
				$dat_chiengi = 1;
			}
		}


		($e_sec,$e_min,$e_hour,$e_day,$e_mon, $e_year) = localtime($auc_end_t);
		$d_sec = sprintf("%02d",$e_sec);
		$d_min = sprintf("%02d",$e_min);
		$d_hour = sprintf("%02d",$e_hour);
		$d_day = sprintf("%02d",$e_day);
		$d_mon = sprintf("%02d",$e_mon +1);
		$d_year = $e_year + 1900;
		$d_datim = "$d_year/$d_mon/$d_day $d_hour:$d_min:$d_sec";
		if($auc_soku eq ""){$auc_soku = "上限無し";}
		if(!$auk_haba){$auk_haba = $syokiagehaba;}
		$puraisu_up = int(($auc_ima + $auk_haba) / $auk_haba) * $auk_haba;

		print <<"EOM";
<tr bgcolor=#ccff33><td>▼商種別</td><td align=center>商品</td><td align=center nowrap>残り</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体</td><td align=center>頭脳</td></tr>
<tr bgcolor=#99ffcc align=center><td>▼$syo_syubetu</td><td>$syo_hinmoku</td><td nowrap>$syo_taikyuu</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>
<tr><td align=left colspan=24 bgcolor="#cccccc">【備考】$syo_comment<br></td></tr>$error_mes
<form method="POST" action="$this_script">
<input type=hidden name=mode value="auction">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=hidden name=no value="$i">
<tr><td colspan=24><table width="100%" border="1" cellspacing="0" cellpadding="5" align=center class=yosumi><tr><td>$auc_name</td><td>即決価格</td><td>始め値</td><td>上げ幅</td><td>現在価格</td><td>プライスアップ</td><td>締め切り時間</td></tr>
<tr><td>$auc_t_name<br></td><td>$auc_soku</td><td>$auc_strat円</td><td>$auk_haba円</td><td>$auc_ima円<td><input type="text" name="touhyou" maxlength="10" value ="$puraisu_up">円<input type="submit" name='up' value="ＵＰ"></td><td>$d_datim</td></tr>
<tr><td colspan="7">一言<input type=text name=com_sanka maxlength=50>$com_sanka</td></tr>
<tr><td colspan="7">$com_syupin</td></tr>
</form>
</table></td></tr>
EOM
		$i++;
	} #foreach
print "<tr><td colspan=24><hr></td></tr>\n";

		print <<"EOM";
<tr><td colspan=24><table width="100%" border="1" cellspacing="0" cellpadding="4" align=center class=yosumi><tr><td>出品者</td>
<td>落札者</td><td>始め値</td><td>落札価格</td><td>開始時刻</td><td>落札時刻</td><td>種別</td><td>品名</td></tr>
EOM
	
	@auc_Keys = map {(split /<>/)[9]} @auc_end_syo; #koko2007/10/29
	@auc_end_syo = @auc_end_syo[sort {@auc_Keys[$b] <=> @auc_Keys[$a]} 0 .. $#auc_Keys]; #koko2007/10/29

	foreach $auc_moto(@auc_end_syo){
		($auc_dat,$syo_dat) = split(/\t\t/,$auc_moto);
		($auc_name,$auc_id,$auc_t_name,$auc_t_id,$auc_soku,$auc_strat,$auk_haba,$auc_ima,$auc_e_tim,$auc_end_t,$auc_rak_tim,$auc_rakusatu,$auc_end,$euc_s_subetu,$euc_s_syohin,$com_syupin,$com_sanka) = split(/<>/,$auc_dat);

		($e_sec,$e_min,$e_hour,$e_day,$e_mon, $e_year) = localtime($auc_e_tim);
		$a_sec = sprintf("%02d",$e_sec);
		$a_min = sprintf("%02d",$e_min);
		$a_hour = sprintf("%02d",$e_hour);
		$a_day = sprintf("%02d",$e_day);
		$a_mon = sprintf("%02d",$e_mon +1);
		$a_year = $e_year + 1900;
		$a_datim = "$a_year/$a_mon/$a_day $a_hour:$a_min:$a_sec";
		($en_sec,$en_min,$en_hour,$en_day,$en_mon, $en_year) = localtime($auc_rak_tim);
		$b_sec = sprintf("%02d",$en_sec);
		$b_min = sprintf("%02d",$en_min);
		$b_hour = sprintf("%02d",$en_hour);
		$b_day = sprintf("%02d",$en_day);
		$b_mon = sprintf("%02d",$en_mon +1);
		$b_year = $en_year + 1900;
		$b_datim = "$b_year/$b_mon/$b_day $b_hour:$b_min:$b_sec";

		print <<"EOM";
<tr><td>$auc_name</td><td>$auc_t_name<br></td><td>$auc_strat<br></td><td>$auc_rakusatu<br></td><td>$a_datim</td><td>$b_datim</td><td>$euc_s_subetu</td><td>$euc_s_syohin</td></tr>
<tr><td colspan="8">$com_sanka</td></tr>
<tr><td colspan="8">$com_syupin</td></tr>
EOM
	}
	print <<"EOM";
</table></td></tr></table>
EOM
#koko2007/10/29
	@auc_Keys = map {(split /<>/)[9]} @auction_dat;#2007/11/02
	@auction_dat = @auction_dat[sort {@auc_Keys[$b] <=> @auc_Keys[$a]} 0 .. $#auc_Keys];#2007/11/02

	if ($#auction_dat+1 >= $max_auc){#2007/11/02
		$#auction_dat = $max_auc -1;#2007/11/02
  		$dat_chiengi = 1;
	} #end2007/10/29
	if($dat_chiengi){
		open(IN,"> $auction_log") || &error("Open Error : $auction_log");
		eval{ flock (IN, 2); };
		print IN @auction_dat;#2007/11/02
		close(IN);
	}


	print <<"EOM";
<div align="right">Edit たっちゃん<div>
EOM
	&hooter("login_view","戻る");
	exit;


}

sub ukewatashi{
	if(!$auc_t_id){&error("mono.cgi エラー auction3")} #koko2007/11/18
	open(AUC,"< ./member/$auc_t_id/mono.cgi") || &error("Open Error : $monokiroku_file");
	eval{ flock (AUC, 1); };
#2007/11/02
	@myitem_hairetu = <AUC>;
	close(AUC);
	if($auc_taikyuu){
		$ii = 0;
		$ch_flagu = 0;
		foreach $tmp (@myitem_hairetu){
			&syouhin_sprit($tmp);
			if($syo_syubetu eq 'ギフト' && $syo_hinmoku eq 'クーポン'){
				$syo_taikyuu += $auc_taikyuu;
				&syouhin_temp;
				$myitem_hairetu[$ii] = $syo_temp;
				$ch_flagu = 1;
				last;
			}
			$ii++;
		}
		if(!$ch_flagu){
			push @myitem_hairetu,$syo_dat;
		}
	}else{
		push @myitem_hairetu,$syo_dat;
	}

	$auc_rak_tim = $auc_end_t;
	$auc_rak_kakaku = $auc_ima;
	$auc_end =1;
	$syo_kounyuubi = $ima_time;
	&syouhin_temp($syo_dat);
	$auc_dat_up = "$auc_name<>$auc_id<>$auc_t_name<>$auc_t_id<>$auc_soku<>$auc_strat<>$auk_haba<>$auc_ima<>$auc_e_tim<>$auc_end_t<>$auc_rak_tim<>$auc_rak_kakaku<>$auc_end<>$euc_s_subetu<>$euc_s_syohin<>$com_syupin<>$com_sanka<>\t\t$syo_temp";

	$auction_dat[$i] = $auc_dat_up;
	$dat_chiengi = 1;

#end2007/11/02
	if(!$auc_t_id){&error("mono.cgi エラー auction4")} #koko2007/11/18
	open(AUC,">./member/$auc_t_id/mono.cgi") || &error("Open Error : $monokiroku_file");
	eval{ flock (AUC, 2); };
	print AUC @myitem_hairetu;
	close(AUC);
	$okane = $auc_ima;
	&openAitelog ($auc_id);
	$aite_bank += $okane;
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("$euc_s_syohin 落札($auc_t_name)","",$okane,$aite_bank,"普",$auc_id,"lock_off");

	&openAitelog ($auc_t_id);
	$aite_bank -= $okane;
	&aite_temp_routin;
	open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
	eval{ flock (OUT, 2); };
	print OUT $aite_k_temp;
	close(OUT);
#ver.1.40ここまで
	&aite_kityou_syori("$euc_s_syohin 落札($auc_t_name)",$okane,"",$aite_bank,"普",$auc_t_id,"lock_off");

#	&news_kiroku("落札","$auc_t_nameさんが、$euc_s_syohinを$auc_rak_kakaku円で落札しました。");#
}



################
sub syupin{
	if(!$k_id){&error("mono.cgi エラー auction5")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;#koko2006/10/20
	close(OUT);

	foreach $data (@myitem_hairetu){
		@aitm_hiretu = split(/<>/,$data);
		if ($aitm_hiretu[0] eq "ギフト商品" || $syo_taikyuu_tani eq "日"){
			push @aitem_giftsyo,$data;
		}elsif ($aitm_hiretu[0] eq "ギフト"){
		#	if($aitm_hiretu[1] eq 'クーポン'){next;}#2007/11/02
			push @aitem_gift,$data;
		}else{
			push @aitem_sonota,$data;
		}
	}
	@alldata = (@aitem_gift,@aitem_sonota);

	&header(gym_style);
	print <<"EOM";
<form method="POST" name=auc action="$this_script">
<input type=hidden name=mode value="syupin_do">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>競売したいアイテムにチェックをいれ、競売指定項目を入れて、競売ボタンを押してください。<br>
競売商品は預かりになります。<br>
競りが終了して売れ残った場合は、出品者に戻されます。<br>
売れた金額は銀行預金から自動的に引き落とされます。</td>
<td  bgcolor=#ff33ff align=center width=35%><h1>オークション</h1></td>
</tr></table><br>
<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
※カロリーは摂取できる数値です。<br>
</font></td></tr>
<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体</td><td align=center>頭脳</td><!-- <td align=center>売却<br>値段</td><td align=center nowrap>　備　考　</td><td align=center nowrap>購入日</td> --></tr>
EOM
	$now_time = time;
	@new_myitem_hairetu = ();
	foreach (@alldata) {
		&syouhin_sprit($_);
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
		}
		if ($syo_taikyuu <=0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
			print "<tr bgcolor=#66ffff><td colspan=23>▼$syo_syubetu</td></tr>";
		}

		if ($syo_taikyuu_tani eq "日"){
			$taikyuu_hyouzi_seikei = "$nokorinissuu日";
			$baikyaku_hyouzi = ($tanka * $nokorinissuu);
		}else{
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
		}

		&byou_hiduke($syo_kounyuubi);

		if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
			$disp_siyukanou = "－";
		}else{$disp_siyukanou = "OK";}

		if(($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && $now_time < $last_syokuzi + ($syokuzi_kankaku*60)){ 
			$disp_siyukanou = "－";
		}
		if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール' && $syo_sake > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート' && $syo_dezato > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク' && $syo_dorinku > time){
			$disp_siyukanou = "－";
		}
#koko2008/06/23
		if(!$baikyaku_hyouzi){
			$baikyaku_hyouzi = ($syo_kokugo+$syo_suugaku+$syo_rika+$syo_syakai+$syo_eigo+$syo_ongaku+$syo_bijutu+$syo_looks+$syo_tairyoku+$syo_kenkou+$syo_speed+$syo_power+$syo_wanryoku+$syo_kyakuryoku+$syo_love+$syo_unique+$syo_etti+$calory_hyouzi*10)*$taikyuu_hyouzi_seikei;
			if(!$baikyaku_hyouzi){
				$baikyaku_hyouzi = 100;
			}else{
				$baikyaku_hyouzi *= 100;
			}
		}

		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=4>$baikyaku_hyouzi円</td><td align=left colspan=19>【 備考 】 $syo_comment</td></tr>";
		if (!($syo_taikyuu <=0)){
			if($disp_siyukanou eq "OK"){
				$disp_radio = "<input type=radio value=\"$syo_syubetu\t$syo_hinmoku\t$baikyaku_hyouzi\t\" name=\"syohinmoku\" onClick=\"document.auc.sokketu.value=$baikyaku_hyouzi\">";#koko2008/06/23
			}else{$disp_radio = "";}
#end2008/06/23
			print <<"EOM";
<tr bgcolor=#99ffcc align=center><td align=left $disp_seru>$disp_radio$syo_hinmoku</td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><!-- <td align=right nowrap>$baikyaku_hyouzi円</td><td align=left>$syo_comment</td><td nowrap>$bh_tukihi</td> --></tr>$disp_com
EOM
		}
		if ($syo_taikyuu > 0){
			$maeno_syo_syubetu = "$syo_syubetu";
		}
	}	#foreach閉じ
	if (! @alldata){print "<tr><td colspan=26>現在所有しているアイテムはありません。</td></tr>";}
	print <<"EOM";
<tr><td colspan=24>
<div align=center>
<table width="75%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr><td>即決価格</td><td>始め値</td><td>締め切り時間</td><td>最低上げ幅</td></tr>
<tr><td><input type="text" name="sokketu" maxlength="10">円
</td><td><input type="text" name="hagimene" maxlength="10">円
</td><td><select name="jikan0"><option value="kyou" selected>今日</option><option value="asu">明日</option></select>
<select name="jikan1"><option value="">-</option><option value="0">00</option><option value="1">01</option><option value="2">02</option>
<option value="3">03</option><option value="4">04</option><option value="5">05</option><option value="6">06</option>
<option value="7">07</option><option value="8">08</option><option value="9">09</option><option value="10">10</option>
<option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option>
<option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option>
<option value="19">19</option><option value="20">20</option><option value="21">21</option><option value="22">22</option>
<option value="23">23</option></select>時
<select name="jikan2"><option value="">-</option><option value="0">00</option><option value="10">10</option>
<option value="20">20</option><option value="30">30</option>
<option value="40">40</option><option value="50">50</option></select>分
</td><td><input type="text" name="agehaba" maxlength="10">円
</td></tr></table><br>
<!--	<input type=hidden name=command value="syousai"> -->
コメント：<input type=text name=com_syupin maxlength=50>50字まで
<input type=submit value="競りに出す"></div></td></tr>
</table></form>
EOM
	&hooter("login_view","戻る");
	exit;
}

sub syupin_do{

	if($in{'hagimene'} =~ /[^0-9]/){&error("数値にミスがあります。1");}
	if($in{'agehaba'} =~ /[^0-9]/){&error("数値にミスがあります。2");}
	if($in{'sokketu'} =~ /[^0-9]/){&error("数値にミスがあります。3");}
	if(!$in{'agehaba'}){$in{'agehaba'} = $syokiagehaba;}
	unless ($in{'hagimene'} >= 0 && $in{'agehaba'} >= 0 && $in{'sokketu'} >= 0){&error("数値にミスがあります。4");}
#koko2008/06/23
	($s_sybetu,$s_hinmoku,$syo_jyogen) = split(/\t/, $in{'syohinmoku'});
	if($s_hinmoku =~ /（独自製品）/){&error("独自製品は出品できません");}
	if($syo_jyogen*10 < $in{'sokketu'}-1){&error("即決価格上限に問題があります。");}
#kokoend
	if($in{'sokketu'} && $in{'hagimene'} + $in{'agehaba'} > $in{'sokketu'}){&error("即決価格に問題があります。");}

	if($auc_jyougen && ($auc_jyougen < $in{'hagimene'} + $in{'agehaba'} || $auc_jyougen < $in{'sokketu'})){
		&error("オークションの上限は$auc_jyougen円とさせていただきます。<br>$in{'hagimene'} + $in{'agehaba'} を変えてください。");
	}elsif($auc_jyougen && !$in{'sokketu'}){
		$in{'sokketu'} = $auc_jyougen;
	}

	if($in{'hagimene'} < $in{'agehaba'}){&error("上げ幅は始め値以下に設定してください。");}
	$now_time = time;
	
	($i_sec, $i_min, $i_hour, $i_day, $i_mon, $i_year) = localtime(time);

	if($in{'jikan2'} ne ''){$i_min = $in{'jikan2'};}else{$i_min = (int($i_min / 10)+1) * 10;}
	if($i_min >= 60){$i_hour++;$i_min -=60;}
	if($in{'jikan1'} ne ''){$i_hour = $in{'jikan1'};}else{++$i_hour;}
	if($i_hour >= 24){$i_day++;$i_hour -= 24;}
	if($in{'jikan0'} eq 'asu'){++$i_day;}
	if($i_day > 31){$i_mon++;$i_day =1;}
	if($i_mon > 11){$i_year++;$i_mon =0;}

	use Time::Local;
	eval{ $s_tim = timelocal(0, $i_min, $i_hour, $i_day, $i_mon, $i_year); };
	if($now_time >= $s_tim){&error("時間設定にミスがあります。");}
	($e_sec,$e_min,$e_hour,$e_day,$e_mon, $e_year) = localtime($s_tim);
	$d_sec = sprintf("%02d",$e_sec);
	$d_min = sprintf("%02d",$e_min);
	$d_hour = sprintf("%02d",$e_hour);
	$d_day = sprintf("%02d",$e_day);
	$d_mon = sprintf("%02d",$e_mon +1);
	$d_year = $e_year + 1900;

	if(!$k_id){&error("mono.cgi エラー auction6")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$i = 0;
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		if($syo_syubetu eq $s_sybetu && $syo_hinmoku eq $s_hinmoku){$s_basyo = $i;$sttayou = 1;last;}
		$i++;
	}
	if($sttayou){
		($syo_item) = splice(@myitem_hairetu,$s_basyo,1);
	}else{
		&error("持ち物にはありません。");
	}
	open(OUT,">$monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @myitem_hairetu;
	close(OUT);

	$auc_dat = "$in{'name'}<>$k_id<><><>$in{'sokketu'}<>$in{'hagimene'}<>$in{'agehaba'}<>$in{'hagimene'}<>$now_time<>$s_tim<><><><>$s_sybetu<>$s_hinmoku<>$in{'com_syupin'}<><br><>";


	$auc_syo ="$auc_dat\t\t$syo_item";

	open(IN,"< $auction_log") || &error("Open Error : $auction_log");
	eval{ flock (IN, 1); };
	@auction_dat = <IN>;
	close(IN);
#koko2008/03/19
#	if ($#auction_dat+1 >= $max_auc){
#		$#auction_dat = $max_auc -1;
#	}
#end
	unshift @auction_dat,$auc_syo;

	open(IN,"> $auction_log") || &error("Open Error : $auction_log");
	eval{ flock (IN, 2); };
	print IN @auction_dat;
	close(IN);

	&header("","sonomati");
	print <<"EOM";
<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
$d_year/$d_mon/$d_day $d_hour:$d_min:$d_sec<br>
即決価格 $in{'sokketu'}<br>
始め値 $in{'hagimene'}<br>
上げ幅 $in{'agehaba'}
商種別 $s_sybetu の $s_hinmoku
の競売を始めました。
</span>
</td></tr></table>
<br>
<form method=POST action="$script">
<input type=hidden name=mode value="login_view">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=town_no value="$in{'town_no'}">
<input type=submit value="戻る">
</form></div>
</body></html>
EOM
	exit;

}
__END__

出品者<>出品者ID<>競売者<>競売者ID<>即決価格<>始め値<>上げ幅<>現在値<>登録時間<>締め切り時間<>落札時間<>落札価格<>落札<>商種別<>商品<>コメント出品者<>コメント競売者<>

($auc_name,$auc_id,$auc_t_name,$auc_t_id,$auc_soku,$auc_strat,$auk_haba,$auc_ima,$auc_e_tim,$auc_end_t,$auc_rak_tim,$auc_rak_kakaku,$auc_end,$euc_s_subetu,$euc_s_syohin,$com_syupin,$com_sanka)
