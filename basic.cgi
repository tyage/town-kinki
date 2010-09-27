#!/usr/bin/perl

################################
# 売却期間の設定(秒)
$uritobasi_kisei = 60;
# 売却時この金額より高いとこの金額になる
$uritobasi_jyougen = 100000000;
# 融資制限
$yuusi_jyougengaku = 300000000;
# 同じカードの時の倍率 0=支払い無し 1=普通と同じ 2=倍になる
$doroubai = 2;
# 銀行送金の上限
$hurikomijyougen = 1000000000000;
# 送金オーバー時、エラーで禁止	'yes' エラー 'no'その他 寄付
$soukingaku_over = 'no';
# １日一相手送金制限
$itinitiseigen = 'yes';
# おやつ(アルコール、デザート、ドリンク)の次の使用時間規制'yes'規制、その他'no'
$oyatu_kisei = 'no';
# ボタンでの表示に切り替え
$botangata = 'yes';
# 履歴表示
$disp_rireki = 'yes';
# 二重使用許可　'yes'二重に使える　'no' 使えない
$nijyu_ok = 'no';
# 人生ゲームへの送金を行う
$soukin_zinsei = 'yes';
#送金先ディレクトリ
$dir_zinsei = './sugoroku';
#１日１回に制限する'yes'
$zinsei_soukin_seigen = 'no';
#制限送金1000000 'yes'
$zinsei_jougen_soukin = 'yes';
################################

$this_script = 'basic.cgi';
require './town_ini.cgi';
require './town_lib.pl';
&decode;

#==========メンテチェック==========#
if($mente_flag == 1 && $in{'admin_pass'} eq "" && $in{'mode'} ne ""){&error("$mente_message")}

#==========制限時間チェック==========#
$seigenyou_now_time = time;
$ato_nanbyou=$koudou_seigen-($seigenyou_now_time - $access_byou);
if($seigenyou_now_time - $access_byou < $koudou_seigen){&error("まだ行動できません。あと$ato_nanbyou秒お待ちください。")}
		
#==========条件分岐==========#
if($in{'mode'} eq "keiba"){&keiba;}
elsif($in{'mode'} eq "byouin"){&byouin;}
elsif($in{'mode'} eq "onsen"){&onsen;}
elsif($in{'mode'} eq "prof"){&prof;}
elsif($in{'mode'} eq "item"){&item;}
elsif($in{'mode'} eq "item_do"){&item_do;}
elsif($in{'mode'} eq "job_change"){&job_change;}
elsif($in{'mode'} eq "job_change_go"){&job_change_go;}
elsif($in{'mode'} eq "do_work"){&do_work;}
elsif($in{'mode'} eq "ginkou"){&ginkou;}
elsif($in{'mode'} eq "ginkoumeisai"){&ginkoumeisai;}
elsif($in{'mode'} eq "ginkoufurikomi"){&ginkoufurikomi;}
elsif($in{'mode'} eq "loan"){&loan;}
elsif($in{'mode'} eq "ginkousoukin"){&ginkousoukin;}
elsif($in{'mode'} eq "zinseisoukin"){&zinseisoukin;}
else{&error("「戻る」ボタンで街に戻ってください");}
	
exit;
	
####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

#---------------銀行-------------------#
sub ginkou {
		&openMylog($in{'k_id'});
		if($in{'azukegaku2'}){
			$in{'azukegaku'}=$in{'azukegaku2'};
		}
				if ($in{'command'} eq "預ける"){
								if($in{'azukegaku'} =~ /[^0-9]/){&error("金額は半角数字で記入してください");}
								if($in{'azukegaku'} <= 0){&error("０円以下のお金は預けられません！");}
								if($in{'azukegaku'} > $money){&error("そんなにお金を持ってないです！");}
								$bank=$bank+$in{'azukegaku'};
								$money=$money-$in{'azukegaku'};
								$message_in = "銀行へお金を$in{'azukegaku'}円預けました。";
								&kityou_syori("預け入れ","",$in{'azukegaku'},$bank,"普");
				}elsif ($in{'command'} eq "おろす"){
								if($in{'orosigaku'} =~ /[^0-9]/){&error("金額は半角数字で記入してください");}
								if($in{'orosigaku'} <= 0){&error("０円以下のお金をおろすことはできません！");}
								if($in{'orosigaku'} > $bank){&error("銀行にそんなに預けてありません！");}
								$bank=$bank-$in{'orosigaku'};
								$money=$money+$in{'orosigaku'};
								$message_in = "銀行からお金を$in{'orosigaku'}円おろしました。";
								&kityou_syori("お引き出し","$in{'orosigaku'}","",$bank,"普");
				}elsif ($in{'command'} eq "スーパー"){
								if($in{'azukegaku'} =~ /[^0-9]/){&error("金額は半角数字で記入してください");}
								$super_azuke_kin = ($in{'azukegaku'}*1000000);
								if($super_azuke_kin > $money){&error("そんなにお金を持ってないです！");}
								$super_teiki=$super_teiki+$super_azuke_kin;
								$money=$money-$super_azuke_kin;
								$message_in = "スーパー定期へお金を$super_azuke_kin円預けました。";
								&kityou_syori("預け入れ","",$in{'azukegaku'}*1000000,$super_teiki,"定");
				}elsif ($in{'command'} eq "解約"){
								$money=$money+$super_teiki;
								$orosumaeno_super_teiki = $super_teiki;
								$message_in = "スーパー定期（$super_teiki円）を解約しました。";
								$super_teiki=0;
								&kityou_syori("解約","$orosumaeno_super_teiki","",$super_teiki,"定");
				}else{
				
#==========銀行画面出力==========#
	&header(ginkou_style);
			if($bank eq  ""){$ima_azuke = "無し";}else{$ima_azuke="$bank円";}
			if($super_teiki > 0){$super_gaku = "（スーパー定期預金額：$super_teiki円）";}
			my $saidai_teiki = int($money * 0.000001);
			if ($saidai_teiki <= 0){$saidai_teiki = "";}
			$zandaka_keisan .= "<option value=>指定額を</option>";
			if ($money > 10000000){$issen = $money - 10000000; $zandaka_keisan .= "<option value=$issen>1000万残して</option>";}
			if ($money > 5000000){$gohyaku = $money - 5000000; $zandaka_keisan .= "<option value=$gohyaku>500万残して</option>";}
			if ($money > 1000000){$hyaku = $money - 1000000; $zandaka_keisan .= "<option value=$hyaku>100万残して</option>";}
			if ($money > 500000){$gojuu = $money - 500000; $zandaka_keisan .= "<option value=$gojuu>50万残して</option>";}
			if ($money > 100000){$juu = $money - 100000; $zandaka_keisan .= "<option value=$juu>10万残して</option>";}
			if ($money > 50000){$juu = $money - 50000; $zandaka_keisan .= "<option value=$juu>5万残して</option>";}
			if ($money > 10000){$iti = $money - 10000; $zandaka_keisan .= "<option value=$iti>1万残して</option>";}
		  
			print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>いらっしゃいませ。<div class="honbun2">●$nameさんの所持金：$money円</div></td>
	<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>銀　行</b></font></td>
	</tr></table><br>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr>
	
	<td width=50% valign=top>
	<span style=font-size:14px;color:#ff3300>■普通口座</span><span class="honbun2">（現在の預け入れ額：$ima_azuke）</span><br><br>
			※普通口座にお金を預けておくと、１日１回0.5％の利息がつきます。また、家を持っていた場合のおさい銭や、お店の商品が売れた時の入金などにも利用されます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkou">
	<input type=hidden name=command value="預ける">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	◆お　預　け <input type=text name=azukegaku value="$money" size=20>円 <select name = "azukegaku2">$zandaka_keisan</select><input type=submit value="預ける">
	</form>
	
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkou">
	<input type=hidden name=command value="おろす">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	◆お引き出し <input type=text name=orosigaku size=20 value="$bank">円 <input type=submit value="引き出す">
	</form>

	<span style=font-size:14px;color:#ff3300>■入出金明細</span><br><br>
		※普通預金の入出金明細を見ることができます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkoumeisai">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=syubetu value="普通預金入出金明細">
	<input type=submit value="入出金明細を見る">
	</form>
	<hr size=1>
	<span style=font-size:14px;color:#ff3300>■振り込み</span><br><br>
		※参加者のメンバー名がわかれば送金することができます。お金は普通口座より引き落とされます。<br>※送金は $hurikomijyougen円までで越えた分は寄付されます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkoufurikomi">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	振込先のお名前 <input type=text name=aitenonamae size=16>
	振り込み金額 <input type=text name=hurikomigaku size=8>円
	<input type=submit value="振り込み">
	</form>
	
<hr size=1><span style=font-size:14px;color:#ff3300>■人生ゲームに送金</span><br><br>
※人生ゲームに送金することができます。お金は普通口座より引き落とされます。1000000円まで何回も送られます。<br>
<form method="POST" action="$this_script">
<input type=hidden name=mode value="zinseisoukin">
<input type=hidden name=name value="$in{'name'}">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=k_id value="$in{'k_id'}">
<input type=hidden name=town_no value="$in{'town_no'}">
送金金額 <input type=text name=sokingaku size=16>円
<input type=submit value="送金">
</form>
	
	</td><td width=50% valign=top>
	
	<span style=font-size:14px;color:#ff3300>■スーパー定期</span><span class="honbun2">$super_gaku</span><br><br>
		※スーパー定期では１日１回１％の利息がつきます。ただし、預け入れ額は100万単位で、お金をおろすさいは解約として全額おろさねばなりません。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkou">
	<input type=hidden name=command value="スーパー">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	◆お　預　け <input type=text name=azukegaku value="$saidai_teiki" size=6> 00万 <input type=submit value="預ける">
	</form>
	
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkou">
	<input type=hidden name=command value="解約">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	◆ご　解　約 <input type=submit value="解約する">
	</form>
	<span style=font-size:14px;color:#ff3300>■スーパー定期明細</span><br><br>
		※スーパー定期の入出金明細を見ることができます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="ginkoumeisai">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=syubetu value="スーパー定期明細">
	<input type=submit value="入出金明細を見る">
	</form>
	<hr size=1>
	<span style=font-size:14px;color:#ff3300>■ローン</span><br><br>
EOM

	if ($loan_kaisuu > 0){
	$loan_zandaka_kei = $loan_nitigaku * $loan_kaisuu;
	print <<"EOM";
	●現在のローン残金＝$loan_zandaka_kei円（$loan_nitigaku円×$loan_kaisuu回）<br>
	※残金を一括返済される場合は下のボタンを押してください。その場合、普通口座より引き落とされます。
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="loan">
	<input type=hidden name=command value="ikkatu_hensai">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="ローンの一括返済">
	</form>
EOM
	}else{
		print <<"EOM";
		※当銀行へのご利用度や収入に応じてお金を借りることができます。一括返済もできます。<br>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="loan">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="融資額の査定">
	</form>
EOM
	}

	print <<"EOM";
	</td></tr>
	</table>
EOM
	&hooter("login_view","戻る");
	exit;
			}

#==========画面出力以外の場合のログ更新処理==========#
					&temp_routin;
					&log_kousin($my_log_file,$k_temp);
					$ginkou_yobidasi = "1";
					&message($message_in,"login_view");

}

#----------銀行振り込み処理----------#
sub ginkoufurikomi {
	if ($in{'command'} ne "from_system"){
		if($in{'hurikomigaku'} <= 0){&error("０円、マイナスの金額は振り込むことができません");}
		if($in{'hurikomigaku'} =~ /[^0-9]/){&error("金額は半角数字で記入してください");}
		if ($bank < $in{'hurikomigaku'}){&error("普通口座に必要なお金が足りません。");}
		if ($name eq $in{'aitenonamae'}){&error("自分宛に振り込むことはできません。");}
	&id_check ($in{'aitenonamae'});
	&openAitelog ($return_id);
		$now_time = time;
		$aite_tatta = int(($now_time - $aite_first_access) / (24 * 60 * 60));
		if ($aite_tatta<7 && $in{'hurikomigaku'}>=1000000){&error("登録後１週間未満の方には１００万円以上振り込めません。");}
		if ($in{'hurikomigaku'} > $hurikomijyougen){
			if ($soukingaku_over eq 'yes'){&error("送金額上限$hurikomijyougen円を越しています。");}
			$furikomi_kifu = $in{'hurikomigaku'} - $hurikomijyougen;
			$in_hurikomigaku = $hurikomijyougen;
		}else{
			$in_hurikomigaku = $in{'hurikomigaku'}
		}
		if ($itinitiseigen eq 'yes'){&soukin_chc;}
	}else{
		$in_hurikomigaku = $in{'hurikomigaku'};
	}

	&id_check ($in{'aitenonamae'});
	&openAitelog ($return_id);

	$aite_bank += $in_hurikomigaku;
	
	if ($in{'command'} ne "from_system"){
		$bank -= $in_hurikomigaku;
		&kityou_syori("振り込み→$in{'aitenonamae'}","$in_hurikomigaku","",$bank,"普");
		if ($furikomi_kifu){
			$bank -= $furikomi_kifu;
			&kityou_syori("寄付","$furikomi_kifu","",$bank,"普");
		}
	}else{
		$in{'name'} = "$admin_name 管理人";
	}
	
	if ($in{'hurikomigaku'} < 0){
		$in{'hurikomigaku'} = abs $in{'hurikomigaku'};
		&aite_kityou_syori("減金←$in{'name'}",$in{'hurikomigaku'},"",$aite_bank,"普",$return_id,"");
	}else{
		&aite_kityou_syori("振り込み←$in{'name'}","",$in_hurikomigaku,$aite_bank,"普",$return_id,"");
	}
	
#==========ログ更新==========#
	&lock;	
	if ($in{'command'} ne "from_system"){
			&temp_routin;
			open(OUT,">$my_log_file") || &error("@$my_log_fileが開けません");
			eval{ flock (OUT, 2); };
			print OUT $k_temp;
			close(OUT);
	}
			
			&aite_temp_routin;
				open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
				eval{ flock (OUT, 2); };
				print OUT $aite_k_temp;
				close(OUT);
	&unlock;
	
	if ($furikomi_kifu){$furikomi_dsp ="<br>$furikomi_kifu円を寄付しました。"}
	if ($in{'command'} ne "from_system"){
		&message("$in{'aitenonamae'}さんの普通口座に$in_hurikomigaku円を振り込みました。$furikomi_dsp","login_view");
	}else{
		&message("$in{'aitenonamae'}さんの普通口座に$in{'hurikomigaku'}円を振り込みました。","itiran","admin.cgi");
	}
}

#----------通帳チェック----------#
sub soukin_chc {
	my (@my_tuutyou);
	&lock;
	$ginkoumeisai_file="./member/$k_id/ginkoumeisai.cgi";
	open(GM,"< $ginkoumeisai_file") || &error("自分の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@my_tuutyou = <GM>;
	close(GM);
	&unlock;

	&time_get;

	foreach (@my_tuutyou) {
		my ($tu_date,$meisai,$soukingaku) = split(/<>/);
		if ($tu_date eq $date && $meisai eq "振り込み→$in{'aitenonamae'}"){
			$total_soukingaku += $soukingaku;
			if ($total_soukingaku + $in_hurikomigaku > $hurikomijyougen){
				&error("今日、この人への送金が上限を超します。<br>送金出来ません。");
			}
		}
	}
}

#----------ローン----------#
sub loan {
	if ($in{'hensai_kaisuu'}){

#==========借り入れ処理==========#
		if ($loan_kaisuu > 0){&error("ローンを完済するまで新しい融資はできません。");}
		my ($nitigaku,$nitigaku_kaisuu) = split(/×/,$in{'hensai_kaisuu'});
		$loan_nitigaku = "$nitigaku";
		$loan_kaisuu = "$nitigaku_kaisuu";
		$bank += $in{'yuusi_kanougaku'};
		&kityou_syori("住宅ローン","",$in{'yuusi_kanougaku'},$bank,"普");
		
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			&message("$in{'yuusi_kanougaku'}円を普通預金口座に振り込みました。","login_view");
	}elsif ($in{'command'} eq "ikkatu_hensai"){
	
#==========一括返済==========#
		$ikkatu_hensai_gaku = $loan_nitigaku * $loan_kaisuu;
		if ($bank < $ikkatu_hensai_gaku){&error("普通口座に十\分な預金がありません");}
		$bank -= $ikkatu_hensai_gaku;
		$loan_nitigaku = 0;
		$loan_kaisuu = 0;
		&kityou_syori("住宅ローン一括返済","$ikkatu_hensai_gaku","",$bank,"普");
		
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			&message("住宅ローンの一括返済をしました。","login_view");
	}else{
	
#==========査定処理画面出力==========#
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);
	foreach  (@job_hairetu) {
			&job_sprit($_);
			if($job_name eq "$job"){
				last;
			}
	}
	$yuusi_kanougaku = int(($job_kyuuyo * ($job_keiken/50) * ($job_kaisuu/50)) + ($bank * 2)+($super_teiki * 2.5));
	$yuusi_kanougaku -= $yuusi_kanougaku % 10000;
	
	if ($yuusi_kanougaku > $yuusi_jyougengaku){$yuusi_kanougaku = $yuusi_jyougengaku}
	
	$kai12 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.05))/12);
	$kai24 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.06))/24);
	$kai36 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.07))/36);
	$kai48 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.08))/48);
	$kai60 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.09))/60);
	$kai72 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.1))/72);
	$kai84 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.11))/84);
	$kai96 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.12))/96);
	$kai108 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.13))/108);
	$kai120 = int(($yuusi_kanougaku + ($yuusi_kanougaku*0.14))/120);
	
	&header(ginkou_style);
	print <<"EOM";
		<table width="400" border="0" cellspacing="0" cellpadding="20" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>
	<div class=dai align=center>ご　査　定</div><hr size=1><br>
	<div class=job_messe>$name様の当銀行へのお預け入れ額や<br>
	ご職業、経験、勤続期間などから査定いたしまして、<br>
	ご融資できます金額は以下の通りとなります。
	<br><br><div class=dai>$yuusi_kanougaku円</div>
	
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="loan">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name=yuusi_kanougaku value="$yuusi_kanougaku">
	ご返済は毎日（ログイン時）、返済回数に応じて5～14%の利子がついた額が普通預金口座より引き落とされます。<br>
	また、完済するまでは次にお金を借りることはできません。

	<select name="hensai_kaisuu">
	<option value="$kai12×12">12回払い（日額$kai12円）</option>
	<option value="$kai24×24">24回払い（日額$kai24円）</option>
	<option value="$kai36×36">36回払い（日額$kai36円）</option>
	<option value="$kai48×48">48回払い（日額$kai48円）</option>
	<option value="$kai60×60">60回払い（日額$kai60円）</option>
	<option value="$kai72×72">72回払い（日額$kai72円）</option>
	<option value="$kai84×84">84回払い（日額$kai84円）</option>
	<option value="$kai96×96">96回払い（日額$kai96円）</option>
	<option value="$kai108×108">108回払い（日額$kai108円）</option>
	<option value="$kai120×120">120回払い（日額$kai120円）</option>
	</select>
	<input type=submit value="借りる">
	</form>
	</td></tr>
	</table>
	<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
	</body></html>
EOM
	exit;
	}
}

#----------銀行明細----------#
sub ginkoumeisai {
	$ginkoumeisai_file="./member/$k_id/ginkoumeisai.cgi";
	if (! -e $ginkoumeisai_file){
		open(GM,">$ginkoumeisai_file") || &error("自分の預金通帳ファイルを作成できません");
		eval{ flock (GM, 2); };
		close(GM);
	}
	open(GM,"< $ginkoumeisai_file") || &error("自分の預金通帳ファイルが開けません");
	eval{ flock (GM, 1); };
	@my_tuutyou = <GM>;
	close(GM);

	&header(ginkou_style);
	print <<"EOM";
	<table width="90%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr class=sita><td colspan=5>■$in{'syubetu'}　※明細は普通預金、スーパー定期合わせて100件まで記帳されます。</td></tr>
	<tr class=sita bgcolor=#cccc99 align=center>
	<td>年　月　日</td><td>お取り引き内容</td><td>出　金　額</td><td>入　金　額</td><td>差し引き残高</td></tr>
EOM
	foreach (@my_tuutyou){
		&ginkou_meisai_sprit($_);
		if ($in{'syubetu'} eq "普通預金入出金明細"){if ($meisai_syubetu ne "普"){next;}}
		if ($in{'syubetu'} eq "スーパー定期明細"){if ($meisai_syubetu ne "定"){next;}}
		
if ($meisai_zandaka =~ /^[-+]?\d\d\d\d+/g) {
  for ($i = pos($meisai_zandaka) - 3, $j = $meisai_zandaka =~ /^[-+]/; $i > $j; $i -= 3) {
	substr($meisai_zandaka, $i, 0) = ',';
  }
}
if ($meisai_hikidasi =~ /^[-+]?\d\d\d\d+/g) {
  for ($i = pos($meisai_hikidasi) - 3, $j = $meisai_hikidasi =~ /^[-+]/; $i > $j; $i -= 3) {
	substr($meisai_hikidasi, $i, 0) = ',';
  }
}
if ($meisai_azuke =~ /^[-+]?\d\d\d\d+/g) {
  for ($i = pos($meisai_azuke) - 3, $j = $meisai_azuke =~ /^[-+]/; $i > $j; $i -= 3) {
	substr($meisai_azuke, $i, 0) = ',';
  }
}

	print <<"EOM";
		<tr class=sita><td>$meisai_date</td><td>$meisai_naiyou</td><td align=right><font color=#ff3333>$meisai_hikidasi</font></td><td align=right><font color=#009933>$meisai_azuke</font></td><td align=right>$meisai_zandaka円</td></tr>
EOM
	}
	print <<"EOM";
		</table>
		<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
		</body></html>
EOM
	exit;
}

#----------競馬----------#
sub keiba {
	my $now_time = time;
my (@umaname)=('◇ダンスパートナー','◇エアグルーヴ','◇ビワハヤヒデ','◇イシノサンデー','◇ジャングルポケット','◇マンハッタンカフェ','◇ノーリーズン','◇オグリキャップ','◇サクラプレジデント','◇エアシャカール','◇ビワハイジ','◇ナリタブライアン','◇テイエムオーシャン','◇トウカイテイオー','◇ローマンエンパイア');
my (@umakakeritu)=('8','28','2','12','16','4','30','3','5');
%umagazou =("◇ダンスパートナー","danpa.gif","◇エアグルーヴ","groove.gif","◇ビワハヤヒデ","hayahide.gif","◇イシノサンデー","ishisun.gif","◇ジャングルポケット","junpoke.gif","◇マンハッタンカフェ","manhattan.gif","◇ノーリーズン","noreason.gif","◇オグリキャップ","oguri.gif","◇サクラプレジデント","sakura_predi.gif","◇エアシャカール","shakur.gif","◇ビワハイジ","heidi.gif","◇ナリタブライアン","brian.gif","◇テイエムオーシャン","tm_ocean.gif","◇トウカイテイオー","tokai_teio.gif","◇ローマンエンパイア","roman.gif");

#==========ランキングファイル読み込み==========#
	open(KR,"< $keibarank_logfile") || &error("Open Error : $keibarank_logfile");
	eval{ flock (KR, 1); };
		@keiba_ranking =<KR>;
	close(KR);
	
		@alldata = @keiba_ranking;
		@keys0 = map {(split /<>/)[1]} @alldata;
		@alldata = @alldata[sort {@keys0[$b] <=> @keys0[$a]} 0 .. $#keys0];

	$i = 0;
	foreach (@alldata){
		($kr_name,$kr_moukegaku,$kr_tounyuugaku,$kr_kakutokugaku,$kr_yobi1,$kr_yobi2,$kr_yobi3,$kr_yobi4)= split(/<>/);
#kr_yobi1 = 最終ゲーム時間
		$rank_html .= "<tr><td>$kr_name</td><td align=right>$kr_moukegaku円</td><td align=right>$kr_tounyuugaku円</td><td align=right>$kr_kakutokugaku円</td></tr>";
		$i ++;
		if ($i >= 10){last;}
	}
	
#==========馬をランダムに並び替え==========#
	@new_entry = ();
	foreach (@umaname){
			my $r = rand @new_entry+1;
			push (@new_entry,$new_entry[$r]);
			$new_entry[$r] = $_;
	}
	
#==========掛け率をランダムに並び替え==========#
	@new_kakeritu = ();
	foreach (@umakakeritu){
			my $s = rand @new_kakeritu+1;
			push (@new_kakeritu,$new_kakeritu[$s]);
			$new_kakeritu[$s] = $_;
	}
	
	foreach (0..5){
		$umaname{$new_entry[$_]} = "$new_kakeritu[$_]";
	}
	
#==========賭ける画面==========#
	if ($in{'command'} eq ""){
	&header(keiba_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffff99>馬券は１枚500円です。購入枚数を入力して「レース開始」ボタンを押してください。２頭まで賭けることができます。<br>
	$nameさんの持ち金：$money円<br>
	※一度に購入できる馬券の枚数は$keiba_gendomaisuu枚までです。<br>
	※$deleteUser日間ゲームしていないユーザーはランキングから削除されます。</td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>競　馬</b></font></td>
	</tr></table><br>
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>

	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="keiba">
	<input type=hidden name=command value="start">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<tr><td valign=top>
	<table cellspacing="0" cellpadding="8" width=100% class=yosumi>
	<tr bgcolor=#99cc66>
	<td align=center colspan=3>本日の出走馬</td></tr>
	<tr bgcolor=#ffff99>
	<td align=center>馬</td><td align=center>オッズ</td><td align=center>購入数</td></tr>
EOM
		foreach (0..5){
				$hid_name = "uma"."$_";
				$hid_kake = "kake"."$_";
				$hid_kane = "kane"."$_";
				print <<"EOM";
			<tr><td>
			<input type=hidden name="$hid_name" value="$new_entry[$_]">
			$new_entry[$_] 
			</td>
			<td align=right>
			<input type=hidden name="$hid_kake" value="$new_kakeritu[$_]">
			$new_kakeritu[$_]倍
			</td>
			<td align=right><input type=text name="$hid_kane" size=10> 枚</td></tr>
EOM
		}
	print <<"EOM";
		<tr><td align=center colspan=3><input type=submit value="レース開始"></td></tr>
		</table></form>
		</td><td  valign=top width=60%>
		<table cellspacing="0" cellpadding="4" class=yosumi width=100%>
		<tr bgcolor=#ff9900><td colspan=4 align=center>
		ギャンブル王ベスト10
		</td></tr>
		<tr bgcolor=#ffffcc><td align=center>名前</td><td align=center>トータル儲け額</td><td align=center>総投入額</td><td align=center>総獲得額</td></tr>
		$rank_html
		</table>
		</tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
	}
	
#==========スタート開始画面==========#
	if ($in{'command'} eq "start"){
	&keibalock;
		$start_html  .= <<"EOM";
	<form method="POST" name=keiba action="$this_script">
	<input type=hidden name=mode value="keiba">
	<input type=hidden name=command value="go">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table border=0 width=620 bgcolor=#cc9933 align=center cellspacing="0" cellpadding="0">
	<tr><td width=20>
	<table border=0 width=20 height=100% bgcolor=#ffff99><tr><td align=center><img src=$img_dir/goal.gif width=11 height=33></td></tr></table>
	</td><td align=right>
	<table border=0 bgcolor=#ffffff><tr><td width=120 align=center>馬</td><td width=40 align=center>オッズ</td><td width=40 align=center>購入</td></tr></table>
	<hr size=2 color=#ffffff>
EOM
	@now_race = ();
	foreach (0..5){
		if($in{'kane'.$_} =~ /[^0-9]/){&keibaunlock; &error("購入数が不適切です。");}
		if ($in{'kane'.$_}){$kaketaumanokazu ++;}
		$kyori = int((rand(60)+10)/(1+($in{'kake'.$_}/70)));
		$keiba_temp = "$in{'uma'.$_}<>$in{'kake'.$_}<>$in{'kane'.$_}<>$kyori<>\n";
		$hikarerugaku += $in{'kane'.$_} * 500;
		$kounyuu_soumaisuu += $in{'kane'.$_};
		push (@now_race,$keiba_temp);
		if ($in{'kane'.$_}){$kakekin = "$in{'kane'.$_}枚";}else{$kakekin = "";}
		$start_html  .=  <<"EOM";
		<table border=0 cellspacing="0" cellpadding="0">
		<tr>
		<td width=$kyori align=left><img src=$img_dir/uma/$umagazou{"$in{'uma'.$_}"} width=30 height=30></td>
		<td width=120>$in{'uma'.$_}</td>
		<td width=40 align=right>$in{'kake'.$_}倍</td>
		<td width=40 align=right>$kakekin</td>
		</tr></table><hr size=2 color=#ffffff noshade>
EOM
	}
	if ($hikarerugaku == 0){&keibaunlock; &error("馬券が購入されていません");}
	if ($money < $hikarerugaku){&keibaunlock; &error("お金が足りません");}
	if ($kounyuu_soumaisuu > $keiba_gendomaisuu){&keibaunlock; &error("一度に購入できる馬券の枚数は$keiba_gendomaisuu枚までです");}
	if ($kaketaumanokazu > 2){&keibaunlock; &error("２頭までしか賭けることができません");}
	&header;
	print <<"EOM";
	$start_html		
	</td><tr></table>
	<br><br>
	<input type=hidden name=count value="$gool">
	</form>
	</body></html>
EOM
	open(KB,">$keiba_logfile")|| &error("Open Error : $keiba_logfile");
	eval{ flock (KB, 2); };
	print KB @now_race;
	close(KB);
	
	$money -= $hikarerugaku;
	
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
	exit;
	
	}
	
#==========ゴーゴー画面==========#
	if ($in{'command'} eq "go"){
	if (!-e $keibalockfile) {&error("時間切れのためレースは棄権扱いとなりました。");}
	open(KB,"< $keiba_logfile")|| &error("Open Error : $keiba_logfile");
	eval{ flock (KB, 1); };
		@keiba_hairetu =<KB>;
	close(KB);
	&header;
		print <<"EOM";
	<form method="POST" name=keiba action="$this_script">
	<input type=hidden name=mode value="keiba">
	<input type=hidden name=command value="go">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table border=0 width=620 bgcolor=#cc9933 align=center cellspacing="0" cellpadding="0">
	<tr><td width=20>
	<table border=0 width=20 height=100% bgcolor=#ffff99><tr><td align=center><img src=$img_dir/goal.gif width=11 height=33></td></tr></table>
	</td><td align=right>
	<table border=0 bgcolor=#ffffff><tr><td width=120 align=center>馬</td><td width=40 align=center>オッズ</td><td width=40 align=center>購入</td></tr></table>
	<hr size=2 color=#ffffff>
EOM
	@now_race = ();
	@kekkahantei = ();
	#+++++１ターン+++++#
	foreach (@keiba_hairetu){
		($umaname,$ods,$kane,$kyori) = split(/<>/);
		$kyori += int((rand(100)+0)/(1+($ods/80)));
		if ($kyori >= 400){$kyori = 400;}
		push (@kekkahantei , $kyori);
		$keiba_temp = "$umaname<>$ods<>$kane<>$kyori<>\n";
		push (@now_race,$keiba_temp);
		if ($kane){$kakekin = "$kane枚";}else{$kakekin = "";}
		print <<"EOM";
		<table border=0 cellspacing="0" cellpadding="0">
		<tr>
		<td width=$kyori align=left><img src=$img_dir/uma/$umagazou{"$umaname"} width=30 height=30></td>
		<td width=120>$umaname</td>
		<td width=40 align=right>$ods倍</td>
		<td width=40 align=right>$kakekin</td>
		</tr></table><hr size=2 color=#ffffff noshade>
EOM
	}
	#+++++結果判定+++++#
	@win_hairetu = ();
	foreach (0..5){
		if ($kekkahantei[$_] >= 400){
			($winner) = split (/<>/ , $now_race[$_] );
			push (@win_hairetu ,$winner);
		}
	}
	#+++++ゴールした場合+++++#
	if (@win_hairetu){
			if (@win_hairetu >=2){
				$syasin_randed=rand($#win_hairetu+1);
				$kekkahappyou = "@win_hairetuがほぼ同時にゴールインしましたが、写真判定の結果、@win_hairetu[$syasin_randed]が１着となりました！";
				$win_uma = "@win_hairetu[$syasin_randed]";
			}else{
				$kekkahappyou ="@win_hairetuが１着でゴールイン！";
				$win_uma = "@win_hairetu";
			}
			foreach (@now_race){
				($umaname,$ods,$kane,$kyori) = split(/<>/);
				if ($umaname eq "$win_uma"){
						$kakutokugaku = $ods * $kane * 500;
						if ($kakutokugaku == 0){
							$kakutokuhyouzi = "残念ながら配当金はありません";
						}else{
						$kakutokuhyouzi = "$kakutokugaku円";
						}
				}
				$soukounyuu += $kane*500;
			}
		$gool = 1;
		print <<"EOM";
		<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
		<div  class=tyuu>$kekkahappyou</div>
		購入金額：$soukounyuu円<br>
		獲得金額：$kakutokuhyouzi
		</td></tr></table><br>
		</td></tr>
		</table>
		<input type=hidden name=count value="$gool">
		</form>
		
	<div align=center><form method=POST action="$this_script">
	<input type=hidden name=mode value="keiba">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=admin_pass value="$in{'admin_pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="再挑戦">
	</form></div>

EOM
		&hooter("login_view","戻る");
		print "</body></html>";

		$money += $kakutokugaku;
		
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
	#+++++ランキングファイル更新+++++#
	open(KR,"< $keibarank_logfile") || &error("Open Error : $keibarank_logfile");
	eval{ flock (KR, 1); };
		@keiba_ranking =<KR>;
	close(KR);
	$kizon_flag=0;
	@new_keiba_ranking = ();
	foreach (@keiba_ranking){
		($kr_name,$kr_moukegaku,$kr_tounyuugaku,$kr_kakutokugaku,$kr_yobi1,$kr_yobi2,$kr_yobi3,$kr_yobi4)= split(/<>/);
		if ($name eq "$kr_name"){
			$kr_tounyuugaku += $soukounyuu;
			$kr_kakutokugaku += $kakutokugaku;
			$kr_moukegaku = $kr_kakutokugaku - $kr_tounyuugaku;
			$kizon_flag=1;
			$kr_yobi1 = $now_time;
		}
		$kr_rank_temp = "$kr_name<>$kr_moukegaku<>$kr_tounyuugaku<>$kr_kakutokugaku<>$kr_yobi1<>$kr_yobi2<>$kr_yobi3<>$kr_yobi4<>\n";
		push (@new_keiba_ranking ,$kr_rank_temp);
	}
	if ($kizon_flag == 0){
		$moukegaku = $kakutokugaku - $soukounyuu;
		$kr_rank_temp = "$name<>$moukegaku<>$soukounyuu<>$kakutokugaku<>$now_time<><><><>\n";
		push  (@new_keiba_ranking ,$kr_rank_temp);
	}
	open(KRO,">$keibarank_logfile")|| &error("Open Error : $keibarank_logfile");
	eval{ flock (KRO, 2); };
	print KRO @new_keiba_ranking;
	close(KRO);
	
	&keibaunlock;
	
	}else{
#==========レース続行==========#
		print <<"EOM";
		</td></tr>
		</table>
		<br><br>
		<input type=hidden name=count value="$gool">
		</form>
		</body></html>
EOM
		open(KB,">$keiba_logfile")|| &error("Open Error : $keiba_logfile");
		eval{ flock (KB, 2); };
		print KB @now_race;
		close(KB);
	}
	exit;
	}
}

#----------競馬用ロック処理----------#
sub keibalock {
	local($retry, $mtime);

#========== 5 / 3分以上古いロックは削除する==========#
	if (-e $keibalockfile) {
		($mtime) = (stat($keibalockfile))[9];
		if ($mtime < time - 180) { &keibaunlock; }
	}

#==========リトライは10回==========#
	$retry = 1;
	while (!mkdir($keibalockfile, 0755)) {
		if (--$retry <= 0) { &error('ただいまレース開催中です。少々お待ちください。'); }
		for (0..50){$i=0;}
	}
	$keibalockflag=1;
}

#----------競馬用アンロック処理----------#
sub keibaunlock {
		open(KB,">$keiba_logfile")|| &error("Open Error : $keiba_logfile");
		eval{ flock (KB, 2); };
		print KB @clear;
		close(KB);
		
#==========ロックディレクトリ削除==========#
	rmdir($keibalockfile);

#==========ロックフラグを解除==========#
	$keibalockflag=0;
}

#----------病院----------#
sub byouin {
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	$motimonokensa = '';
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_hinmoku eq '健康保険'){
			$motimonokensa = 1;
			last;
		}
	}

	if ($in{'command'}){
		if ($in{'command'} eq "風邪ぎみ"){
			$tiryouhi = 18000;
		}elsif($in{'command'} eq "風邪"){
			$tiryouhi = 28000;
		}elsif($in{'command'} eq "下痢"){
			$tiryouhi = 32000;
		}elsif($in{'command'} eq "肺炎"){
			$tiryouhi = 35000;
		}elsif($in{'command'} eq "結核"){
			$tiryouhi = 48000;
		}elsif($in{'command'} eq "癌"){
			$tiryouhi = 88000;
		}elsif($in{'command'} eq "元気"){
			$tiryouhi = 10000;
		}
	if ($motimonokensa){$tiryouhi=int ($tiryouhi / 3);}
	
		if ($money < $tiryouhi){&error("お金が足りません");}
			$money -= $tiryouhi;
			$byouki_sisuu = 50;
			$byoumei = "";
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			&message("病気の治療をしました。もうこれで安心です。病気のさいはまた当院をご利用くださいませ。","login_view");
	}
	
#==========表示==========#
	&header(ginkou_style);
			if($bank eq  ""){$ima_azuke = "無し";}else{$ima_azuke="$bank円";}
			if($super_teiki > 0){$super_gaku = "●スーパー定期預金額：$super_teiki円";}
			print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>いらっしゃいませ。どんな病気もたちどころに治します。<br><font color="red">健康保険があると治療費が３分の１になります！</font></td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>病　院</b></font></td>
	</tr></table><br>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi><tr>
	<td>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="byouin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
EOM
	if ($byoumei eq "風邪ぎみ"){
		print <<"EOM";
		<div class=honbun4 align=center>
		軽度の風邪のようですね。<br>注射を打っておきましょう。<br>治療費に18000円かかります。<br>よろしいですか？<br>
		<input type=hidden name=command value="風邪ぎみ">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","ぼったくりっぽいのでやめる");
	}elsif($byoumei eq "風邪"){
		print <<"EOM";
		<div class=honbun4 align=center>
		ふむふむ。単なる風邪ですね。注射を打てばすぐに治りますよ。<br>治療費に28000円かかります。<br>よろしいですね？<br>
		<input type=hidden name=command value="風邪">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","ぼったくりっぽいのでやめる");
	}elsif($byoumei eq "下痢"){
		print <<"EOM";
		<div class=honbun4 align=center>
		ふむふむ。単なる下痢ですね。お尻に注射を打てばすぐに治りますよ。<br>治療費に32000円かかります。<br>よろしいですね？<br>
		<input type=hidden name=command value="下痢">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","ぼったくりっぽいのでやめる");
	}elsif($byoumei eq "肺炎"){
		print <<"EOM";
		<div class=honbun4 align=center>
		うーむ。肺炎ですね。風邪を引いてから無理するからですよ。<br>でもご安心ください。<br>うちの注射を打てばすぐに治りますよ。<br>費用はたった35000円です。<br>安いもんですよね。<br>
		<input type=hidden name=command value="肺炎">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","自力で治すから結構\です");
	}elsif($byoumei eq "結核"){
		print <<"EOM";
		<div class=honbun4 align=center>
		むむ。。いけませんなぁ。結核のようです。。<br>もっと早くうちへ来てくれれば良かったのに。。<br>でももう大丈夫。本来入院が必要ですが、<br>うちの注射を打てばあっという間に治ってしまいますよ。<br>ただし費用は48000円かかります。。<br>まぁ、これで結核が治れば安いものかと。。。<br>
		<input type=hidden name=command value="結核">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","高い！やめる！");
	}elsif($byoumei eq "脳腫瘍"){
		print <<"EOM";
		<div class=honbun4 align=center>
		ま、まずいですよぉ。当病院の的確な検査の結果、脳腫瘍と診断されました。。<br>このままでは生死にかかわります。<br>ただちに手術しましょう！<br>そうすればすぐに治ります。<br>費用は64000円かかりますが、お金のことをとやかく言ってる場合ではありません。<br>
		<input type=hidden name=command value="脳腫瘍">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","高すぎだ！やめる！");
	}elsif($byoumei eq "癌"){
		print <<"EOM";
		<div class=honbun4 align=center>
		ガーン。。なんちゃって。い、いや、大変なことになりました！！<br>あなたは癌です！これは治るから告知しているのですよ。<br>ただし、真っ先に手術が必要です！<br>この街のブラックジャックと呼ばれた私の腕にかかれば<br>癌ですらすぐに治すことが可\能\です。<br>ただし費用はちょっとかかりますが。。。<br>大負けに負けて88000円です。<br>でもこのままでは死んでしまいます！<br>迷ってるヒマはありません！<br>
		<input type=hidden name=command value="癌">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","死んでもいい！そんな金払えん！");
	}elsif($byoumei eq ""){
		print <<"EOM";
		<div class=honbun4 align=center>
		どこも悪いところはないようです。<br>念のため注射を打っておきますか？<br>10000円かかりますが。。<br><br>
		<input type=hidden name=command value="元気">
		<input type=submit value="お願いします"></form>
		</div>
EOM
		&hooter("login_view","金を取られる前に退散する");
	}else{
			print <<"EOM";
		<div class=honbun4 align=center>
		むむむむむ？？　これは。。。私の手に負えない病気です。。。<br>どこか他を当たってくださいませ。</div>
EOM
		&hooter("login_view","失意のまま病院を後にする");
	}
	
	print <<"EOM";
	</td></tr></table>
EOM
	&hooter("login_view","戻る");
	exit;
}

#----------温泉----------#
sub onsen {

#==========パワーのMAX値計算==========#
	$energy_max = int(($looks/12) + ($tairyoku/4) + ($kenkou/4) + ($speed/8) + ($power/8) + ($wanryoku/8) + ($kyakuryoku/8))+1;
	$nou_energy_max = int(($kokugo/6) + ($suugaku/6) + ($rika/6) + ($syakai/6) + ($eigo/6)+ ($ongaku/6)+ ($bijutu/6))+1;
	if ($in{'onsec'} eq ""){$in{'onsec'} = time;}
	$jisa = $in{'onsec'} - time;
	my ($ima0_time) = $in{'onsec'};
	my ($date_sec) = time;

	if($energy_max >= $nou_energy_max){
		$tokubetu_times = int($energy_max / 50);
		if($tokubetu_times < 2){$tokubetu_times = 2;}
	}else{
		$tokubetu_times = int($nou_energy_max / 50);
		if($tokubetu_times < 2){$tokubetu_times = 2;}
	}
	$tokubetuburo_hiyou = $tokubetu_times*100;

	if (!$in{'onsensyurui'}){

		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$matu_times)+1;#
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$matu_times)+1;#

		$ima_energy = int(($energy_max - $energy)/$onsen_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_f0 = int($ima_energy/60);
		$energy_f1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$onsen_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_f0 =int($ima_nou/60);
		$nou_energy_f1=$ima_nou%60;

		$ima_energy = int(($energy_max - $energy)/$tokubetu_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_t0=int($ima_energy/60);
		$energy_t1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$tokubetu_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_t0=int($ima_nou/60);
		$nou_energy_t1=$ima_nou%60;

		$ima_energy = int(($energy_max - $energy)/$matu_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_m0 = int($ima_energy / 60);
		$energy_m1=$ima_energy % 60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$matu_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_m0=int($ima_nou / 60);
		$nou_energy_m1=$ima_nou % 60;

		$ima_energy = int(($energy_max - $energy)/$take_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_tk0 = int($ima_energy/60);
		$energy_tk1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$take_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_tk0=int($ima_nou/60);
		$nou_energy_tk1=$ima_nou%60;

		$ima_energy = int(($energy_max - $energy)/$ume_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_u0 =int($ima_energy/60);
		$energy_u1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$ume_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_u0 = int($ima_nou/60);
		$nou_energy_u1=$ima_nou%60;

		$ima_energy = int(($energy_max - $energy)/$dou_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_d0 =int($ima_energy/60);
		$energy_d1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$dou_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_d0 = int($ima_nou/60);
		$nou_energy_d1=$ima_nou%60;
		
		$ima_energy = int(($energy_max - $energy)/$gin_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_g0 =int($ima_energy/60);
		$energy_g1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$gin_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_g0 = int($ima_nou/60);
		$nou_energy_g1=$ima_nou%60;

		$ima_energy = int(($energy_max - $energy)/$kin_times*$sintai_kaihuku);
		if($ima_energy < 0){$ima_energy = 0;}
		$energy_k0 =int($ima_energy/60);
		$energy_k1=$ima_energy%60;
		$ima_nou = int(($nou_energy_max - $nou_energy)/$kin_times*$zunou_kaihuku);
		if($ima_nou < 0){$ima_nou = 0;}
		$nou_energy_k0 = int($ima_nou/60);
		$nou_energy_k1=$ima_nou%60;

#==========表示==========#
		&ori_header("background-color : #336699; background-repeat : no-repeat; background-position : center center;");
		print <<"EOM";
	<table  border=0  cellspacing="5" cellpadding="0" width=100% height=70%><tr><td valign=top>
	<h2 align=center>風呂の選択</h2>
<table  border=0  cellspacing="2" cellpadding="0" width=450 align=center bgcolor=#ffffcc><tr><td>
<table border=0 align=center>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="futuu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="普通風呂に入る">
	</form>
</td><td>$nyuuyokuryou円</td><td>$onsen_times倍</td><td><font color="#ff0000">$energy_f0分$energy_f1秒</font></td><td><font color="#0000ff">$nou_energy_f0分$nou_energy_f1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="特別風呂に入る">
	</form>
</td><td>$tokubetuburo_hiyou円</td><td>$tokubetu_times倍</td><td><font color="#ff0000">$energy_t0分$energy_t1秒</font></td><td><font color="#0000ff">$nou_energy_t0分$nou_energy_t1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_ume">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="梅風呂に入る">
	</form>
</td><td>$ume_hiyou円</td><td>$ume_times倍</td><td><font color="#ff0000">$energy_u0分$energy_u1秒</font></td><td><font color="#0000ff">$nou_energy_u0分$nou_energy_u1秒</font><td>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_take">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="竹風呂に入る">
	</form>
</td><td>$take_hiyou円</td><td>$take_times倍</td><td><font color="#ff0000">$energy_tk0分$energy_tk1秒</font></td><td><font color="#0000ff">$nou_energy_tk0分$nou_energy_tk1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_matu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="松風呂に入る">
	</form>
</td><td>$matu_hiyou円</td><td>$matu_times倍</td><td><font color="#ff0000">$energy_m0分$energy_m1秒</font></td><td><font color="#0000ff">$nou_energy_m0分$nou_energy_m1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_dou">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="銅風呂に入る">
	</form>
</td><td>$dou_hiyou円</td><td>$dou_times倍</td><td><font color="#ff0000">$energy_d0分$energy_d1秒</font></td><td><font color="#0000ff">$nou_energy_d0分$nou_energy_d1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_gin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="銀風呂に入る">
	</form>
</td><td>$gin_hiyou円</td><td>$gin_times倍</td><td><font color="#ff0000">$energy_k0分$energy_k1秒</font></td><td><font color="#0000ff">$nou_energy_k0分$nou_energy_k1秒</font><td>
</tr>
<tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_kin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="金風呂に入る">
	</form>
</td><td>$kin_hiyou円</td><td>$kin_times倍</td><td><font color="#ff0000">$energy_k0分$energy_k1秒</font></td><td><font color="#0000ff">$nou_energy_k0分$nou_energy_k1秒</font><td>
</tr>
</table>
</td></table>
EOM

		&hooter("login_view","街へ戻る");
		exit;
	}

#==========入ったときの処理==========#
	if ($in{'onsensyurui'} eq "koukyuu"){
		#+++++高級の風呂+++++#
		$onsensyurui = "two";
		$o_kakaruhiyou = $tokubetuburo_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$tokubetu_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$tokubetu_times)+1;
		$ima_energy = $ima0_time + int(($energy_max - $energy)/$tokubetu_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$tokubetu_times*$zunou_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
	}elsif ($in{'onsensyurui'} eq "koukyuu_matu"){
		#+++++松の風呂+++++#
		$onsensyurui = "five";
		$o_kakaruhiyou = $matu_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$matu_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$matu_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$matu_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$matu_times*$zunou_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
	}elsif ($in{'onsensyurui'} eq "koukyuu_take"){
		#+++++竹の風呂+++++#
		$onsensyurui = "fo";
		$o_kakaruhiyou = $take_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$take_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$take_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$take_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$take_times*$zunou_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
	}elsif ($in{'onsensyurui'} eq "koukyuu_ume"){
		#+++++梅の風呂+++++#
		$onsensyurui = "three";
		$o_kakaruhiyou = $ume_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$ume_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$ume_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$ume_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$ume_times*$zunou_kaihuku) + 1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
	}elsif ($in{'onsensyurui'} eq "special_dou"){
		#+++++銅の風呂+++++#
		$onsensyurui = "six";
		$o_kakaruhiyou = $dou_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$dou_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$dou_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$dou_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$dou_times*$zunou_kaihuku) + 1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
		
		$tairyku_up = int(rand(10)+1);
		$kenkou_up = int(rand(10)+1);
		if ($tairyku_up <= 3){
			$tairyoku += $tairyku_up;
			$disp .= "体力が$tairyku_upＵＰしました！<br>";
		}
		if ($kenkou_up <= 3){
			$kenkou += $kenkou_up;
			$disp .= "健康が$kenkou_upＵＰしました！<br>";
		}
	}elsif ($in{'onsensyurui'} eq "special_gin"){
		#+++++銀の風呂+++++#
		$onsensyurui = "seven";
		$o_kakaruhiyou = $gin_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$gin_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$gin_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$gin_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$gin_times*$zunou_kaihuku) + 1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
		
		$looks_up = int(rand(20)+1);
		$tairyoku_up = int(rand(20)+1);
		$kenkou_up = int(rand(20)+1);
		$speed_up = int(rand(20)+1);
		$power_up = int(rand(20)+1);
		$wanryoku_up = int(rand(20)+1);
		$kyakuryoku_up = int(rand(20)+1);

		if ($looks_up <= 10){
			$looks += $looks_up;
			$disp .= "ルックスが$looks_upＵＰしました！<br>";
		}
		if ($tairyku_up <= 10){
			$tairyoku += $tairyku_up;
			$disp .= "体力が$tairyku_upＵＰしました！<br>";
		}
		if ($kenkou_up <= 10){
			$kenkou += $kenkou_up;
			$disp .= "健康が$kenkou_upＵＰしました！<br>";
		}
		if ($spped_up <= 10){
			$speed += $speed_up;
			$disp .= "スピードが$speed_upＵＰしました！<br>";
		}
		if ($power_up <= 10){
			$power += $power_up;
			$disp .= "パワーが$power_upＵＰしました！<br>";
		}
		if ($wanryoku_up <= 10){
			$wanryoku += $wanryoku_up;
			$disp .= "腕力が$wanryoku_upＵＰしました！<br>";
		}
		if ($kyakuryoku_up <= 10){
			$$kyakuryoku += $$kyakuryoku_up;
			$disp .= "脚力が$$kyakuryoku_upＵＰしました！<br>";
		}
	}elsif ($in{'onsensyurui'} eq "special_kin"){
		#+++++金の風呂+++++#
		$onsensyurui = "eight";
		$o_kakaruhiyou = $kin_hiyou;
		$energy = $energy + int(($date_sec - $last_ene_time)/$sintai_kaihuku*$kin_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time)/$zunou_kaihuku*$kin_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy)/$kin_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy)/$kin_times*$zunou_kaihuku) + 1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
		
		$looks_up = int(rand(20)+1);
		$tairyoku_up = int(rand(20)+1);
		$kenkou_up = int(rand(20)+1);
		$speed_up = int(rand(20)+1);
		$power_up = int(rand(20)+1);
		$wanryoku_up = int(rand(20)+1);
		$kyakuryoku_up = int(rand(20)+1);

		$kokugo_up = int(rand(20)+1);
		$suugaku_up = int(rand(20)+1);
		$rika_up = int(rand(20)+1);
		$syakai_up = int(rand(20)+1);
		$eigo_up = int(rand(20)+1);
		$ongaku_up = int(rand(20)+1);
		$bijutu_up = int(rand(20)+1);

		$love_up = int(rand(20)+1);
		$unique_up = int(rand(20)+1);
		$etti_up = int(rand(20)+1);

		if ($looks_up <= 10){
			$looks += $looks_up;
			$disp .= "ルックスが$looks_upＵＰしました！<br>";
		}
		if ($tairyku_up <= 10){
			$tairyoku += $tairyku_up;
			$disp .= "体力が$tairyku_upＵＰしました！<br>";
		}
		if ($kenkou_up <= 10){
			$kenkou += $kenkou_up;
			$disp .= "健康が$kenkou_upＵＰしました！<br>";
		}
		if ($spped_up <= 10){
			$speed += $speed_up;
			$disp .= "スピードが$speed_upＵＰしました！<br>";
		}
		if ($power_up <= 10){
			$power += $power_up;
			$disp .= "パワーが$power_upＵＰしました！<br>";
		}
		if ($wanryoku_up <= 10){
			$wanryoku += $wanryoku_up;
			$disp .= "腕力が$wanryoku_upＵＰしました！<br>";
		}
		if ($kyakuryoku_up <= 10){
			$$kyakuryoku += $$kyakuryoku_up;
			$disp .= "脚力が$$kyakuryoku_upＵＰしました！<br>";
		}
		if ($kokugo_up <= 10){
			$kokugo += $kokugo_up;
			$disp .= "国語が$kokugo_upＵＰしました！<br>";
		}
		if ($suugaku_up <= 10){
			$suugaku += $suugaku_up;
			$disp .= "数学が$suugaku_upＵＰしました！<br>";
		}
		if ($rika_up <= 10){
			$rika += $rika_up;
			$disp .= "理科が$rika_upＵＰしました！<br>";
		}
		if ($syakai_up <= 10){
			$syakai += $syakai_up;
			$disp .= "社会が$syakai_upＵＰしました！<br>";
		}
		if ($eigo_up <= 10){
			$eigo += $eigo_up;
			$disp .= "英語が$eigo_upＵＰしました！<br>";
		}
		if ($ongaku_up <= 10){
			$ongaku += $ongaku_up;
			$disp .= "音楽が$ongaku_upＵＰしました！<br>";
		}
		if ($bijutu_up <= 10){
			$bijutu += $bijutu_up;
			$disp .= "美術が$bijutu_upＵＰしました！<br>";
		}
		if ($love_up <= 10){
			$love += $love_up;
			$disp .= "ＬＯＶＥ度が$love_upＵＰしました！<br>";
		}
		if ($unique_up <= 10){
			$unique += $unique_up;
			$disp .= "面白さが$unique_upＵＰしました！<br>";
		}
		if ($etti_up <= 10){
			$etti += $etti_up;
			$disp .= "エッチが$etti_upＵＰしました！<br>";
		}
	}elsif ($in{'onsensyurui'} eq "futuu"){
		#+++++普通の風呂+++++#
		$onsensyurui = "one";
		$o_kakaruhiyou = $nyuuyokuryou;
		$energy = $energy + int(($date_sec - $last_ene_time) / $sintai_kaihuku*$onsen_times)+1;
		$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time) / $zunou_kaihuku*$onsen_times)+1;

		$ima_energy = $ima0_time + int(($energy_max - $energy) / $onsen_times*$sintai_kaihuku)+1;
		($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_energy+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_ene_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";

		$ima_nou = $ima0_time + int(($nou_energy_max - $nou_energy) / $onsen_times*$zunou_kaihuku)+1;
($sec_dis,$min_dis,$hour_dis,$mday_dis,$mon_dis,$year_dis,) = localtime($ima_nou+1);
		$year_dis += 1900;
		$mon_dis++;
		$ima_nou_dis = "$year_dis $mon_dis $mday_dis $hour_dis $min_dis $sec_dis";
	}
		#+++++ログ更新+++++#
	$last_ene_time= $date_sec;
	if($energy > $energy_max){$energy = $energy_max;}
	if($energy < 0){$energy = 0;}
	$last_nouene_time= $date_sec;
	if($nou_energy > $nou_energy_max){$nou_energy = $nou_energy_max;}
	if($nou_energy < 0){$nou_energy = 0;}
	$money -= $o_kakaruhiyou;
	
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
			
		#+++++表示+++++#
	my $gazou_bangou =int(rand($on_gazou_suu))+1;
	my $onsen_gazou = "$gazou_bangou".".jpg";
	&ori_header("background-color : #336699; background-repeat : no-repeat; background-position : center center; background-image : url( $img_dir/onsen/$onsen_gazou)");
	print <<"EOM";
	<table  border=0  cellspacing="5" cellpadding="0" width=100% height=70%><tr><td valign=top>
	<br><table  border=0  cellspacing="2" cellpadding="0" width=370 align=center bgcolor=#ffffcc><tr><td>
EOM
	if ($in{'onsensyurui'} eq "koukyuu"){
		print "<div style=\"font-size:11px\">特別風呂入浴中のため通常の$tokubetu_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>";
	}elsif($in{'onsensyurui'} eq "koukyuu_matu"){
		print "<div style=\"font-size:11px\">松風呂入浴中のため通常の$matu_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>";
	}elsif($in{'onsensyurui'} eq "koukyuu_take"){
		print "<div style=\"font-size:11px\">竹風呂入浴中のため通常の$take_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>";
	}elsif($in{'onsensyurui'} eq "koukyuu_ume"){
		print "<div style=\"font-size:11px\">梅風呂入浴中のため通常の$ume_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>";
	}elsif($in{'onsensyurui'} eq "special_dou"){
		print "<div style=\"font-size:11px\">銅風呂入浴中のため通常の$dou_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。<br><font color=\"red\">$disp</font></div>";
	}elsif($in{'onsensyurui'} eq "special_gin"){
		print "<div style=\"font-size:11px\">銀風呂入浴中のため通常の$gin_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。<br><font color=\"red\">$disp</font></div>";
	}elsif($in{'onsensyurui'} eq "special_kin"){
		print "<div style=\"font-size:11px\">金風呂入浴中のため通常の$kin_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。<br><font color=\"red\">$disp</font></div>";
	}elsif ($in{'onsensyurui'} eq "futuu"){
		print "<div style=\"font-size:11px\">普通風呂入浴中のため通常の$onsen_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>";
	}else{
	print <<"EOM";
	<div style="font-size:11px">入浴中は通常の$onsen_times倍の早さでパワーが回復します。時差：$jisa
	<br>※$tokubetuburo_hiyou円払って特別風呂に入ると$tokubetu_times倍の早さでパワーが回復します。<br>※$matu_hiyou円払って松風呂に入ると$matu_times倍の早さでパワーが回復します。<br>※$take_hiyou円払って竹風呂に入ると$take_times倍の早さでパワーが回復します。<br>※$ume_hiyou円払って梅風呂に入ると$ume_times倍の早さでパワーが回復します。<br>※$dou_hiyou円払って銅風呂に入ると$dou_times倍の早さでパワーが回復します。<br>※$gin_hiyou円払って銀風呂に入ると$gin_times倍の早さでパワーが回復します。<br>※$kin_hiyou円払って金風呂に入ると$kin_times倍の早さでパワーが回復します。<br>※リロードするとお金をとられます。</div>
EOM
	}
	print <<"EOM";
	</td></tr></table><br>
	<table  border=0  cellspacing="5" cellpadding="0" width=200 align=center><tr><td>
	<div align=center><img src="$img_dir/nyuuyoku.gif" width="110" height="30"></div>
<tr bgcolor="#ffffff"><td>
<form name="powa">
<input type=hidden name=ene value="$ima_ene_dis">
<input type=hidden name=nou value="$ima_nou_dis">
身体パワー：<input type="text" size="16" name="tairyoku_pw"><br>
頭脳パワー：<input type="text" size="16" name="zunou_pw">
</td></tr></form>
	</td></tr></table>
	</td></tr></table>
	<div align=center>
EOM

	if ($in{'onsensyurui'} ne "koukyuu" && $in{'onsensyurui'} ne "koukyuu_matu" && $in{'onsensyurui'} ne "koukyuu_take" && $in{'onsensyurui'} ne "koukyuu_ume" && $in{'onsensyurui'} ne "special_dou" && $kakidashino eq 'yes'){
	print <<"EOM";
<script type="text/javascript">
<!--
function on_sec(){
	myDate = Math.round((new Date()).getTime()/1000);
	document.onsen.onsec.value = myDate;
}
//-->
</script>

<table border=0 align=center><tr><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="特別風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_matu">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="松風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_take">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="竹風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="koukyuu_ume">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="梅風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_dou">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="銅風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_gin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="銀風呂に入る" onClick="on_sec()">
	</form>
</td><td>
	<form method=POST name=onsen action="$this_script">
	<input type=hidden name=mode value="onsen">
	<input type=hidden name=onsec value="">
	<input type=hidden name=onsensyurui value="special_kin">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="金風呂に入る" onClick="on_sec()">
	</form>
</td></tr></table>
EOM
	}

	print <<"EOM";
	<form method=POST name=onsen action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=onsec value="">
	<input type=hidden name=iiyudane value="$onsensyurui">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="お湯から出る" onClick="on_sec()">
	</form>
	</div>
	</body></html>
EOM
	exit;
	
}

#----------プロフィール----------#
sub prof {
	open(IN,"< $profile_file") || &error("Open Error : $profile_file");
	eval{ flock (IN, 1); };
	@alldata=<IN>;
	$total_touroku_suu = @alldata;
	close(IN);

#==========登録フォームの出力==========#
	if ($in{'command'} eq "touroku_form"){
		&prof_form;
		exit;
	}
	
#==========登録の場合==========#
	if ($in{'command'} eq "touroku"){
		$atta_flag=0;
		@new_alldata = ();
		foreach (@alldata){
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
		#+++++修正の場合+++++#
			if ($name eq "$pro_name"){next;} 
			push (@new_alldata,$_);
		}

		my($new_entry) = "$name<>$in{'pro_sex'}<>$in{'pro_age'}<>$in{'pro_addr'}<>$in{'pro_p1'}<>$in{'pro_p2'}<>$in{'pro_p3'}<>$in{'pro_p4'}<>$in{'pro_p5'}<>$in{'pro_p6'}<>$in{'pro_p7'}<>$in{'pro_p8'}<>$in{'pro_p9'}<>$in{'pro_p10'}<>$in{'pro_p11'}<>$in{'pro_p12'}<>$in{'pro_p13'}<>$in{'pro_p14'}<>$in{'pro_p15'}<>$in{'pro_p16'}<>$in{'pro_p17'}<>$in{'pro_p18'}<>$in{'pro_p19'}<>$in{'pro_p20'}<>\n";
		unshift (@new_alldata,$new_entry);
		
	&lock;
	open(OUT,">$profile_file") || &error("$profile_fileに書き込めません");
	eval{ flock (OUT, 2); };
	print OUT @new_alldata;
	close(OUT);
	&unlock;
	&message("プロフィールの登録を行いました。","prof","basic.cgi");
	exit;
	}
	
		#+++++表示+++++#
	&header(prof_style);
		print <<"EOM";
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>バーチャルではなく、本当のプロフィールを登録したり、閲覧したりする場所です。現在登録数：$total_touroku_suu人
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="prof">
	<input type=hidden name=command value="touroku_form">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="プロフィール登録＆修正">
	</form>
	</td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>プロフィール</b></font></td>
	</td></tr></table><br>

	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center bgcolor=#ffcc66>
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="prof">
	<input type=hidden name=command value="easySerch">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<tr>
EOM
		#+++++検索フォーム+++++#
	print "<td>名　前 <input type=text name=serch_name size=20></td>\n";
	print "<td><select name=sex>\n";
	print "<option value=\"99\">性別\n";
		for($i=1;$i<@sex_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'sex'} eq $sex_array[$i]);
				print ($option,$sex_array[$i]);
		}
	print "</select></td>\n";
	
	print "<td><select name=age>\n";
	print "<option value=\"99\">年齢\n";
		for($i=1;$i<@age_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'age'} eq $age_array[$i]);
				print ($option,$age_array[$i]);
		}
	print "</select></td>\n";
	
	print "<td><select name=address>\n";
	print "<option value=\"99\">住所\n";
		for($i=1;$i<@address_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'address'} eq $address_array[$i]);
				print ($option,$address_array[$i]);
		}
	print "</select></td>\n";
	
	print "<td valign=top nowrap>\n";
	print "<select name=p1>\n";
	print "<option value=\"99\">$prof_name1\n";
		for($i=1;$i<@prof_array1;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p1'} eq $prof_array1[$i]);
				print ($option,$prof_array1[$i]);
		}
	print "</select></td></tr><tr>\n";
	
	print "<td valign=top nowrap>\n";
	print "<select name=p2>\n";
	print "<option value=\"99\">$prof_name2\n";
		for($i=1;$i<@prof_array2;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p2'} eq $prof_array2[$i]);
				print ($option,$prof_array2[$i]);
		}
	print "</select></td>\n";
	
	print "<td valign=top nowrap>\n";
	print "<select name=p3>\n";
	print "<option value=\"99\" selected>$prof_name3\n";
		for($i=1;$i<@prof_array3;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p3'} eq $prof_array3[$i]);
				print ($option,$prof_array3[$i]);
		}
	print "</select></td>\n";
	
	print "<td valign=top nowrap>\n";
	print "<select name=p4>\n";
	print "<option value=\"99\" selected>$prof_name4\n";
		for($i=1;$i<@prof_array4;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p4'} eq $prof_array4[$i]);
				print ($option,$prof_array4[$i]);
		}
	print "</select></td>\n";
	
	print "<td valign=top nowrap>\n";
	print "<select name=p5>\n";
	print "<option value=\"99\" selected>$prof_name5\n";
		for($i=1;$i<@prof_array5;$i++){
				my $option='<option>';
				$option='<option selected>' if($in{'p5'} eq $prof_array5[$i]);
				print ($option,$prof_array5[$i]);
		}

	print <<"EOM";
	</select></td>
	<td>
	<input type=submit value=" 検索する ">
	</form>
	  </td>
	</tr>
  </table><br>
EOM
	&hooter("login_view","街へ戻る");
	
	
#==========簡易検索の場合==========#
		if ($in{'command'} eq "easySerch"){
			$i=0;
			@newrank = ();
			foreach (@alldata) {
				($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
				if ($in{'serch_name'} ne "" && $in{'serch_name'} ne $pro_name) { next; }
				if ($in{'sex'} != 99 && $in{'sex'} ne $pro_sex) { next; }
				if ($in{'age'} != 99 && $in{'age'} ne $pro_age) { next; }		
				if ($in{'address'} != 99 && $in{'address'} ne $pro_addr) { next; }
				if ($in{'p1'} != 99 && $in{'p1'} ne $pro_p1) { next; }
				if ($in{'p2'} != 99 && $in{'p2'} ne $pro_p2) { next; }
				if ($in{'p3'} != 99 && $in{'p3'} ne $pro_p3) { next; }
				if ($in{'p4'} != 99 && $in{'p4'} ne $pro_p4) { next; }
				if ($in{'p5'} != 99 && $in{'p5'} ne $pro_p5) { next; }
				$i++;
				push(@newrank,$_);
			}
			@alldata=@newrank;
			print "<div align=center class=sub2>条件にヒットしたのは$i件です。</div><br>";
			&hooter("prof","全て表\示","basic.cgi");
		}
		
	$page=$in{'page'};	
	if ($page eq "") { $page = 0; }
	$i3=0;
		#+++++ログ表示処理+++++#
		foreach (@alldata) {
			($pro_name,$pro_sex,$pro_age,$pro_addr,$pro_p1,$pro_p2,$pro_p3,$pro_p4,$pro_p5,$pro_p6,$pro_p7,$pro_p8,$pro_p9,$pro_p10,$pro_p11,$pro_p12,$pro_p13,$pro_p14,$pro_p15,$pro_p16,$pro_p17,$pro_p18,$pro_p19,$pro_p20)= split(/<>/);
			@my_prof_hairetu = split(/<>/);
		$i3++;
		if ($i3 < $page + 1) { next; }
		if ($i3 > $page + $hyouzi_max_grobal) { last; }
		
			if($pro_sex eq "男"){
					$sex_style="border: #99ccff; border-style: solid; border-width: 3px; background-color:#ffffcc";
			}elsif($pro_sex eq "女"){
					$sex_style="border: #ff9999; border-style: solid; border-width: 3px; background-color:#ffffcc";
			}else{
					$sex_style="border: #cccccc; border-style: solid; border-width: 3px; background-color:#ffffcc";
			}
			
			print "<table style=\"$sex_style\" align=center width=450>";
			$i=1;
			foreach (@my_prof_hairetu){
					$_ =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target=\"_blank\">$2<\/a>/g;
					if ($i == 1){$pr_koumokumei ="名前";}
					elsif ($i == 2){$pr_koumokumei ="性別";}
					elsif ($i == 3){$pr_koumokumei ="年齢";}
					elsif ($i == 4){$pr_koumokumei ="住所";}
					elsif ($i == 5){$pr_koumokumei ="$prof_name1";}
					elsif ($i == 6){$pr_koumokumei ="$prof_name2";}
					elsif ($i == 7){$pr_koumokumei ="$prof_name3";}
					elsif ($i == 8){$pr_koumokumei ="$prof_name4";}
					elsif ($i == 9){$pr_koumokumei ="$prof_name5";}
					else {$pr_koumokumei = $kijutu_prof[$i-10];}
				if ($_ ne "" && $_ ne "\n"){
					print <<"EOM";
					<tr><td align=right width=120><div class=honbun2>$pr_koumokumei</div></td>
					<td>：$_</td></tr>
EOM
				}
					$i ++; 
		}
		
			print <<"EOM";
	<tr><td colspan=2 align=center><form method="POST" action="$script">
	<input type=hidden name=mode value="mail_sousin">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=hidden name="sousinsaki_name" value="$pro_name">
	<input type=submit value="メッセージ送信"></form>
	</td></tr>
	</table><br>
EOM

		}

		$next = $page + $hyouzi_max_grobal;
		$back = $page - $hyouzi_max_grobal;
		print "<div align=center><table border=0><tr>";
		if ($back >= 0) {
		#+++++検索の場合のボタン+++++#
				if($in{'command'} eq "easySerch"){
					print <<"EOM";
			<form method=POST action="$this_script">
			<input type=hidden name=mode value="prof">
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
			<input type=hidden name=page value="$back">
			<input type=submit value="BACK">
			</form>
EOM
				}else{
		#+++++通常の場合+++++#
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="prof">
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
			<input type=hidden name=mode value="prof">
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
			<input type=hidden name=page value="$next">
			<input type=submit value="NEXT">
</form>
EOM
				}else{
					print <<"EOM";
			<td><form method="POST" action="$this_script">
			<input type=hidden name=mode value="prof">
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

#----------登録フォーム----------#
sub prof_form {
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
	
#==========表示==========#
	&header(prof_style);
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="prof">
	<input type=hidden name=command value="touroku">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>公開したい項目のみ選択または記述し、その他は空白のままでOKです。修正・更新はいつでもできます。
	</td>
	<td  bgcolor=#ff6633 align=center width=35%><div style="font-size:13px; color:#ffffff">プロフィール登録</div>
	</td></tr></table><br>
	
	<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr><td>
EOM

print '性別<br><select name="pro_sex">';
		for($i=0;$i<@sex_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($pro_sex eq $sex_array[$i]);
				print ($option,$sex_array[$i]);
		}
		print '</select></td><td>';

		print ' 年齢<br><select name="pro_age">';
		for($i=0;$i<@age_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($pro_age eq $age_array[$i]);
				print ($option,$age_array[$i]);
		}
		print '</select></td><td>';


		print ' 住所<br><select name="pro_addr">';
		for($i=0;$i<@address_array;$i++){
				my $option='<option>';
				$option='<option selected>' if($pro_addr eq $address_array[$i]);
				print ($option,$address_array[$i]);
		}
		print '</select></td><td>';

 		print "$prof_name1<br><select name=\"pro_p1\">";
		for($i=0;$i<@prof_array1;$i++){
				$option='<option>';
				$option='<option selected>' if($pro_p1 eq $prof_array1[$i]);
				print ($option,$prof_array1[$i]);
		}
		print '</select></td></tr><tr><td>';

		print "$prof_name2<br><select name=\"pro_p2\">";
		for($i=0;$i<@prof_array2;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p2 eq $prof_array2[$i]);
				print ($option,$prof_array2[$i]);
		}
		print '</select></td><td>';
 
 		print "$prof_name3<br><select name=\"pro_p3\">";
		for($i=0;$i<@prof_array3;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p3 eq $prof_array3[$i]);
				print ($option,$prof_array3[$i]);
		}
		print '</select></td><td>';
 
 		print "$prof_name4<br><select name=\"pro_p4\">";
		for($i=0;$i<@prof_array4;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p4 eq $prof_array4[$i]);
				print ($option,$prof_array4[$i]);
		}
		print '</select></td><td>';
 
 		print "$prof_name5<br><select name=\"pro_p5\">";
		for($i=0;$i<@prof_array5;$i++){
				$option=' <option>';
				$option='<option selected>' if($pro_p5 eq $prof_array5[$i]);
				print ($option,$prof_array5[$i]);
		}
		print '</select></td></tr>';
		$i = 6;
		$i2=9;
		foreach (@kijutu_prof){
			print "<tr><td align=right>$_</td><td colspan=3><input type=text name=pro_p$i size=80 value=$my_prof_hairetu[$i2]></td></tr>\n";
			$i ++;
			$i2 ++;
		}
		print <<"EOM";
	<tr><td colspan=4 align=center>
	<input type=submit value=" O K "><br>
	</td></tr></table>
	</form>
		
EOM
	&hooter("prof","戻る","basic.cgi");
}

#----------アイテム----------#
sub item {
	if(!$k_id){&error("mono.cgi エラー basic1")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	
	$i = 0;
	@aitem_giftsyo = ();
	@aitem_sonota = ();
	foreach $data (@myitem_hairetu){
		$aitm_hiretu = (split(/<>/,$data))[0];
		$kuka_basyo = (split(/<>/,$data))[9];
		if ($kuka_basyo =~ /食料品/ and $aitm_hiretu eq "ギフト商品"){
			$aitm_hiretu = "食料品";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "食料品";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		if ($kuka_basyo =~ /ファ/ and $aitm_hiretu  eq "ギフト商品"){
			$aitm_hiretu = "ファーストフード";
			&syouhin_sprit($myitem_hairetu[$i]);
			$syo_syubetu = "ファーストフード";
			&syouhin_temp;
			$myitem_hairetu[$i] = $syo_temp;
		}
		$i++;
		if($aitm_hiretu eq "武器" or $aitm_hiretu eq "防具" or $aitm_hiretu eq "魔法" or $aitm_hiretu eq "御守"){
			push @soubihin,$data;
		}
		if ($aitm_hiretu eq "ギフト商品"){
			push @aitem_giftsyo,$data;
		}else{
			push @aitem_sonota,$data;
		}
	}
	@keys0 = map {(split /<>/)[21]} @aitem_giftsyo;
	@itemgift = @aitem_giftsyo[sort {@keys0[$a] <=> @keys0[$b]} 0 .. $#keys0];
	@keys0 = map {(split /<>/)[0]} @aitem_sonota;
	@itemsonota = @aitem_sonota[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];
	@alldata = (@itemgift,@itemsonota);
	
#==========表示==========#
	&header(item_style);
	if ($botangata ne "yes"){
		print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item_do">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
EOM
	}
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>使用したいアイテムにチェックをいれ、「使用する」か「売却する」を選んでOKボタンを押してください。<br>
	※備考に（※アイコン）とある商品は、持っていることで新しいアイコンが現れます。「使用」してしまうと無くなってしまい効果も消えますのでご注意ください。<br>
	※自分で購入した「ギフト」はメール送信画面のセレクトメニューに現れます。このリストには表\示されません。<br>
	現在の$nameさんの身体エネルギー：$energy　頭脳エネルギー：$nou_energy</td>
	<td bgcolor="#ffcc00" align=center width=300><font color="#ffffff" size="5"><b>アイテム</b></font></td>
	</tr></table><br>
	
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=27><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○回なら使用できる回数、○日なら使用できる日数です。<br>
	※カロリーは摂取できる数値です。<br>
	</font></td></tr>
EOM

	if ($botangata ne "yes"){
		print <<"EOM";
	<tr><td colspan=27>
	<div align=center>
	<select name="command">
	<option value="siyou">使用する</option>
	<option value="baikyaku">売却する</option>
	</select>
EOM
	}
	print <<"EOM";
		<tr bgcolor=#ccff33><td align=center nowrap>商品</td><td align=center nowrap>残り</td><td>使用</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td><td align=center>売却<br>値段</td><td align=center nowrap>購入日</td></tr>
EOM
	$now_time = time;
	@new_myitem_hairetu = ();
	@shiyouzumi = ();
	foreach (@alldata) {
		&syouhin_sprit($_);
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
		}
		if($syo_syubetu eq "ギフト"){next;}
		if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
			push @shiyouzumi,$syo_hinmoku;
		}
	}
	
	@shiyozumi_hin = ();
	@shiyozumi_syu = ();
	@new_myitem_hairetu = ();
	foreach (@alldata) {
		&syouhin_sprit($_);
		if ($syo_taikyuu_tani eq "日"){
			$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
			$nokorinissuu = $syo_taikyuu - $keikanissuu;
			if ($nokorinissuu <= 0){next;}
		}
		
		if ($syo_taikyuu <=0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		if ($syo_syubetu ne "ギフト"){
		if($syo_cal ne "0" || $syo_cal ne ""){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "<div align=center>ー</div>";}
		if($syo_kankaku <= 0){$syo_kankaku = "<div align=center>ー</div>";}
		if ($maeno_syo_syubetu ne "$syo_syubetu" && $syo_taikyuu > 0){
				if ($no_disp){
							if ($botangata ne "yes"){
				print <<"EOM";
	<tr><td colspan=27>
	<div align=center>
	<input type=submit value=" O K "></div></td></tr>
EOM
							}
				}else{$no_disp =1;}
				print "<tr bgcolor=#ffff66><td colspan=27>▼$syo_syubetu</td></tr>";
		}
		
		if ($syo_taikyuu_tani eq "日"){
			$taikyuu_hyouzi_seikei = "$nokorinissuu日";
			$baikyaku_hyouzi = ($tanka * $nokorinissuu);
		}else{
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
			$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
		}
		
		&byou_hiduke($syo_kounyuubi);
		$disp_siyukanou = "";
		if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
			$disp_nokori_time = $syo_siyou_date + ($syo_kankaku*60)-$now_time;
			if($disp_nokori_time < 60*3){$mosugu =1;}else{$mosugu =0;}
			$myminitu = int($disp_nokori_time / 60);
			$mysec = $disp_nokori_time % 60;
			if($myminitu){
				$disp_nokori_time = "<b>$myminitu分$mysec秒</b>";
			}else{
				$disp_nokori_time = "<b>$mysec秒</b>";
			}
			$disp_siyukanou = "－";
			push @shiyozumi_hin,$syo_hinmoku;
			push @shiyozumi_syu,$syo_syubetu;
		}else{
			$disp_nokori_time = "";
			$i=0;
			if($nijyu_ok eq 'yes'){
				foreach $tmpo(@shiyozumi_hin){
					if ($syo_hinmoku eq $tmpo && $shiyozumi_syu[$i] eq $syo_syubetu && $syo_syubetu eq 'ギフト商品'){
						$disp_siyukanou = "－";
					}
					$i++;
				}
			}else{
				foreach $tmpo2(@shiyouzumi){
					if ($syo_hinmoku eq $tmpo2){
						$disp_siyukanou = "－";
						last;
					}
				}
			}
			if (!$disp_siyukanou){
				$disp_siyukanou = "OK";
				$disp_ok = '<font color="#0000ff">●</font>';
			}
		}
		
		if(($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード") && $now_time < $last_syokuzi + ($syokuzi_kankaku*60)){ 
			$disp_siyukanou = "－";
			$disp_nokori_time = $last_syokuzi + ($syokuzi_kankaku*60)-$now_time;
			if($disp_nokori_time < 60*3){$mosugu =1;}else{$mosugu =0;}
			$myminitu = int($disp_nokori_time / 60);
			$mysec = $disp_nokori_time % 60;
			if($myminitu){
				$disp_nokori_time = "<b>$myminitu分$mysec秒</b>";
			}else{
				$disp_nokori_time = "<b>$mysec秒</b>";
			}
		}
		if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール' && $syo_sake > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート' && $syo_dezato > time){
			$disp_siyukanou = "－";
		}elsif ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク' && $syo_dorinku > time){
			$disp_siyukanou = "－";
		}
		
		if ($disp_siyukanou eq '－'){$disp_ok = "<font color=\"#ff0000\">×</font>";}
		
		if ($syo_comment || $disp_nokori_time){
			if($disp_siyukanou eq '－' && $mosugu ==0){
				$disp_seru = "rowspan=\"2\"";
				$disp_com = "<tr bgcolor=#cccccc><td colspan=3 bgcolor=#ff00ff>$disp_nokori_time</td><td align=left colspan=22>【 備考 】 $syo_comment</td></tr>";
			}elsif($mosugu == 1 && $disp_siyukanou eq '－'){
				$disp_seru = "rowspan=\"2\"";
				$disp_com = "<tr bgcolor=#cccccc><td colspan=3 bgcolor=#00ff00>$disp_nokori_time</td><td align=left colspan=22>【 備考 】 $syo_comment</td></tr>";
			}else{
				$disp_seru = "rowspan=\"2\"";
				$disp_com = "<tr bgcolor=#cccccc><td colspan=3></td><td align=left colspan=22>【 備考 】 $syo_comment</td></tr>";
			}
		}else{
			$disp_seru = "";
			$disp_com = "";
			$mosugu = 0;
		}
		if (!($syo_taikyuu <=0)){
		
		if (time() >= $syo_kounyuubi + $uritobasi_kisei){
			$baikykukanou = "<input type=radio value=\"baikyaku\" name=\"command\">売却";
		}else{$baikykukanou ="";}

		if ($disp_siyukanou eq 'OK'){
			if ($botangata eq "yes"){
				$display = "<form method=\"POST\" action=\"$this_script\"><input type=hidden name=mode value=\"item_do\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=k_id value=\"$in{'k_id'}\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=hidden value=\"$syo_hinmoku\t$syo_syubetu\" name=\"syo_hinmoku\"><input type=submit value=\"使用\"><input type=radio value=\"siyou\" name=\"command\" checked>使用$baikykukanou</form>";
			}else{
				$display = "<input type=radio value=\"$syo_hinmoku\t$syo_syubetu\" name=\"syo_hinmoku\">";
			}
		}else{
			$display = "";
		}
		print <<"EOM";
		<tr bgcolor=#ccff99 align=center><td nowrap align=left $disp_seru>$display$syo_hinmoku</td><td nowrap>$taikyuu_hyouzi_seikei</td><td>$disp_ok</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td><td align=right nowrap>$baikyaku_hyouzi円</td><td nowrap>$bh_tukihi</td></tr>$disp_com
EOM
		}
				if ($syo_taikyuu > 0){
				$maeno_syo_syubetu = "$syo_syubetu";
				}
		}
		
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}
	foreach(@soubihin){
		unshift (@new_myitem_hairetu,$_);
	}
	
	if (! @alldata){print "<tr><td colspan=27>現在所有しているアイテムはありません。</td></tr>";}
	
	if ($botangata ne 'yes'){
		print <<"EOM";
	<tr><td colspan=27>
	<div align=center>
	<input type=submit value=" O K "></div></td></form></tr>
EOM
	}
	print "</table>";
	
#==========自分の所有物ファイルを更新==========#
			&lock;
			open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close(OUT);
		  
			$loop_count = 0;
			while ($loop_count <= 10){
				for (0..50){$i=0;}
				@f_stat_b = stat($monokiroku_file);
				$size_f = $f_stat_b[7];
				if ($size_f == 0 && @new_myitem_hairetu ne ""){
					open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
					eval{ flock (OUT, 2); };
					print OUT @new_myitem_hairetu;
					close (OUT);
				}else{
					last;
				}
				$loop_count++;
			}
		  
			&unlock;
	&hooter("login_view","戻る");
	exit;
}

#----------アイテム使用----------#
sub item_do {
	if ($in{'syo_hinmoku'} eq ""){&error("アイテムが選ばれていません。");}
	($in_syo_hinmoku,$in_syo_syubetu) = split(/\t/,$in{'syo_hinmoku'});
	if(!$k_id){&error("mono.cgi エラー basic2")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$siyouzumi_flag = 0;
	@new_myitem_hairetu =();
	foreach  (@myitem_hairetu) {
		&syouhin_sprit($_);	
		if($aitm_hiretu eq "武器" or $aitm_hiretu eq "防具" or $aitm_hiretu eq "魔法" or $aitm_hiretu eq "御守"){
			push @soubihin,$_;
		}
		if ($in_syo_hinmoku eq "$syo_hinmoku" && $in_syo_syubetu eq $syo_syubetu && $syo_syubetu ne "ギフト"){
		
#==========使用の場合==========#
			if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < time()){next;}
			if ($in{'command'} eq "siyou" && $siyouzumi_flag == 0){
				$siyouzumi_flag = 1;
				$now_time = time;
				if ($syo_syubetu eq "食料品" || $syo_syubetu eq "ファーストフード"){
					if($now_time < $last_syokuzi + ($syokuzi_kankaku*60)){
						$sinamono_min = int(($last_syokuzi + $syokuzi_kankaku*60 - $now_time) / 60);
						$sinamono_sec = ($last_syokuzi + $syokuzi_kankaku*60 - $now_time) % 60;
						&error("まだ食事できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
					}
					$print_messe .= "●$in_syo_hinmokuを食べました。<br>";
					$last_syokuzi = $now_time;
				}else{
					$print_messe .= "●$in_syo_hinmokuを使用しました。<br>";
				}
		  
				if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール' && $syo_sake <= time){
					$syo_sake = $syo_kankaku * 60 + time;
				}elsif($oyatu_kisei eq 'yes' && $syo_syubetu eq 'アルコール'){
					$matitime = $syo_sake - time;
					$sinamono_min = int($matitime / 60);
					$sinamono_sec = $matitime % 60;
					&error("間隔が短いためまだ使用できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
				}
				if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート' && $syo_dezato <= time){
					$syo_dezato = $syo_kankaku * 60 + time;
				}elsif($oyatu_kisei eq 'yes' && $syo_syubetu eq 'デザート'){
					$matitime = $syo_dezato - time;
					$sinamono_min = int($matitime / 60);
					$sinamono_sec = $matitime % 60;
					&error("間隔が短いためまだ使用できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
				}
				if ($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク' && $syo_dorinku <= time){
					$syo_dorinku = $syo_kankaku * 60 + time;
				}elsif($oyatu_kisei eq 'yes' && $syo_syubetu eq 'ドリンク'){
					$matitime = $syo_dorinku - time;
					$sinamono_min = int($matitime / 60);
					$sinamono_sec = $matitime % 60;
					&error("間隔が短いためまだ使用できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
				}
				if($syo_siyou_date + ($syo_kankaku*60) > $now_time){
					$sinamono_min = int(($syo_siyou_date + ($syo_kankaku*60) -$now_time) / 60);
					$sinamono_sec = ($syo_siyou_date + ($syo_kankaku*60) -$now_time) % 60;
					&error("間隔が短いためまだ使用できません。<br>$sinamono_min分 $sinamono_sec秒お待ちください。");
				}
				if($energy < $syo_sintai_syouhi){&error("身体パワーが足りません。");}
				if($nou_energy < $syo_zunou_syouhi){&error("頭脳パワーが足りません。");}
			 
				if ($in_syo_hinmoku eq $syo_hinmoku && $syo_hinmoku eq 'ランダム品'){
					$randam_frag = 1;

					$b_kokugo = $syo_kokugo;
					$syo_kokugo = int(rand($syo_kokugo + 1));
					$b_suugaku = $syo_suugaku;
					$syo_suugaku = int(rand($syo_suugaku + 1));
					$b_rika = $syo_rika;
					$syo_rika = int(rand($syo_rika + 1));
					$b_syakai = $syo_syakai;
					$syo_syakai = int(rand($syo_syakai + 1));
					$b_eigo = $syo_eigo;
					$syo_eigo = int(rand($syo_eigo + 1));
					$b_ongaku = $syo_ongaku;
					$syo_ongaku = int(rand($syo_ongaku + 1));
					$b_bijutu = $syo_bijutu;
					$syo_bijutu = int(rand($syo_bijutu + 1));
					$b_looks = $syo_looks;
					$syo_looks = int(rand($syo_looks + 1));
					$b_tairyoku = $syo_tairyoku;
					$syo_tairyoku = int(rand($syo_tairyoku + 1));
					$b_kenkou = $syo_kenkou;
					$syo_kenkou = int(rand($syo_kenkou + 1));
					$b_speed = $syo_speed;
					$syo_speed = int(rand($syo_speed + 1));
					$b_power = $syo_power;
					$syo_power = int(rand($syo_power + 1));
					$b_wanryoku = $syo_wanryoku;
					$syo_wanryoku = int(rand($syo_wanryoku + 1));
					$b_kyakuryoku = $syo_kyakuryoku;
					$syo_kyakuryoku = int(rand($syo_kyakuryoku + 1));
					$b_love = $syo_love;
					$syo_love = int(rand($syo_love + 1));
					$b_unique = $syo_unique;
					$syo_unique = int(rand($syo_unique + 1));
					$b_etti = $syo_etti;
					$syo_etti = int(rand($syo_etti + 1));
				}

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

				if ($randam_frag == 1){
					$syo_kokugo = $b_kokugo;
					$syo_suugaku = $b_suugaku;
					$syo_rika = $b_rika;
					$syo_syakai = $b_syakai;
					$syo_eigo = $b_eigo;
					$syo_ongaku = $b_ongaku;
					$syo_bijutu = $b_bijutu;
					$syo_looks = $b_looks;
					$syo_tairyoku = $b_tairyoku;
					$syo_kenkou = $b_kenkou;
					$syo_speed = $b_speed;
					$syo_power = $b_power;
					$syo_wanryoku = $b_wanryoku;
					$syo_kyakuryoku = $b_kyakuryoku;
					$syo_love = $b_love;
					$syo_unique = $b_unique;
					$syo_etti = $b_etti;
				}
		#+++++効果の設定+++++#
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
				if ($syo_taikyuu_tani eq "回"){
					$syo_taikyuu -- ;
				}
			
#==========売却の場合==========#
			}elsif($in{'command'} eq "baikyaku" && $siyouzumi_flag == 0){
				$now_time = time;
				if ($now_time < $syo_kounyuubi + $uritobasi_kisei){
					$print_messe .= "●$in_syo_hinmokuの売却は未だ出来ません。";
				}else{
					if ($syo_taikyuu_tani eq "日"){
						$keikanissuu = int (($now_time - $syo_kounyuubi) / (60*60*24));
						$nokorinissuu = $syo_taikyuu - $keikanissuu;
						$baikyaku_hyouzi = ($tanka * $nokorinissuu);
					}else{
						$baikyaku_hyouzi = ($tanka * $syo_taikyuu);
					}
					if ($syo_siyou_date + ($syo_kankaku*60) > $now_time){&error("$in_syo_hinmokuの売却は未だ出来ません。");}
					 $siyouzumi_flag = 1;
					if ($baikyaku_hyouzi > $uritobasi_jyougen){
						$baikyaku_hyouzi = $uritobasi_jyougen;
					}
					$money += $baikyaku_hyouzi;
					$print_messe .= "●$in_syo_hinmokuを売却し、$baikyaku_hyouzi円を得ました。";
					next;
				}	
			}
		}
		if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		&syouhin_temp;
		push (@new_myitem_hairetu,$syo_temp);
	}

	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	foreach(@soubihin){
		unshift (@new_myitem_hairetu,$_);
	}
#==========自分の所有物ファイルを更新==========#
	&lock;
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
	
	$loop_count = 0;
	while ($loop_count <= 10){
		for (0..50){$i=0;}
		@f_stat_b = stat($monokiroku_file);
		$size_f = $f_stat_b[7];
		if ($size_f == 0 && @new_myitem_hairetu ne ""){
			open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
			eval{ flock (OUT, 2); };
			print OUT @new_myitem_hairetu;
			close (OUT);
		}else{
			last;
		}
		$loop_count++;
	}
	
	if (!$print_messe){$print_messe = "持っていません";}
	&unlock;

#==========BMIをチェック==========#
	$taijuu = sprintf ("%.1f",$taijuu);
	&check_BMI($sintyou,$taijuu);
	
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
$print_messe<br>
身長：$sintyou cm<br>
体重：$taijuu kg<br>
ＢＭＩ：$BMI（$taikei）<br>
</span>
</td></tr></table>
<br>

	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="item">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="アイテム使用">
	</form>
	<a href=\"javascript:history.back()\"> [前の画面に戻る] </a>
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

#----------職業安定所----------#
sub job_change {
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);
	
#==========BMIをチェック==========#
	$taijuu = sprintf ("%.1f",$taijuu);
	&check_BMI($sintyou,$taijuu);
	
#==========条件に満たない職業を可能リストから排除==========#
	foreach (@job_hairetu){
		&job_sprit($_);
		if($kokugo < $job_kokugo){next;}
		if($suugaku < $job_suugaku){next;}
		if($rika < $job_rika){next;}
		if($syakai < $job_syakai){next;}
		if($eigo < $job_eigo){next;}
		if($ongaku < $job_ongaku){next;}
		if($bijutu < $job_bijutu){next;}
		if($BMI < $job_BMI_min){next;}
		if ($job_BMI_max) { if($BMI > $job_BMI_max){next;}}
		if($looks < $job_looks){next;}
		if($tairyoku < $job_tairyoku){next;}
		if($kenkou < $job_kenkou){next;}
		if($speed < $job_speed){next;}
		if($power < $job_power){next;}
		if($wanryoku < $job_wanryoku){next;}
		if($kyakuryoku < $job_kyakuryoku){next;}
		if($love < $job_love){next;}
		if($unique < $job_unique){next;}
		if($etti < $job_etti){next;}
		if ($job_sex) {if($sex ne "$job_sex"){next;}}
		if($sintyou < $job_sintyou){next;}
		if ($job_syurui) {if($job_syurui ne $jobsyu){next;}}
		if($job_rank) {$job_hosi = "*" x ($job_rank-1);}
		
		$job_option .="<option value=$job_no>$job_name$job_hosi</option>";
	}
	if ($job_option eq ""){$job_option = "<option value=\"\">現在就ける職業はありません</option>";}
	
	&header(job_style);
	print <<"EOM";
	<form method="POST" action="$this_script">
	<input type=hidden name=mode value="job_change_go">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="95%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi><tr>
	<td bgcolor=#ffffff>必要なパラメータ、条件を満たしていればその職業に就くことができます。自分のなりたい職業めざして、勉強、トレーニングなどに励みましょう。尚、転職をすると経験値、出勤回数は0に戻ります。<br>
	※職業のレベルが15を超えるとその職業をマスターしたことになり、よりレベルアップした職業が出現することがあります（職業名のあとの「*」がレベルを表\します）。
	</td>
	<td bgcolor="#333333" align=center width=300><font color="#ffffff" size="5"><b>ハローワーク</b></font></td>
	</tr>
	<tr><td colspan=2>
	<span class="tyuu">$nameさんが就職可能\な職業</span><img src=$img_dir/space.gif width=10 height=1>
	<select name="job_sentaku">
	$job_option
	</select><img src=$img_dir/space.gif width=10 height=1>
	 <input type=submit value="この職業に就く">
	 </td></tr></table></form>
EOM

	if($sex eq "m") {$sex = "男";}else{$sex = "女";}
	
	print <<"EOM";
	<table width="95%" border="0" cellspacing="1" cellpadding="4" align=center class=yosumi>
	<tr><td colspan=25><font color=#336699>凡例：(国)＝国語、(数)＝数学、(理)＝理科、(社)＝社会、(英)＝英語、(音)＝音楽、(美)＝美術、(ル)＝ルックス、(体)＝体力、(健)＝健康、(ス)＝スピード、(パ)＝パワー、(腕)＝腕力、(脚)＝脚力、(H)＝エッチ</font></td></tr>
	<tr bgcolor=#ff9933 align=center><td nowrap rowspan=2>職業</td><td colspan=17>必要なパラメータ</td><td align=center colspan=3>条　件</td><td rowspan=2 align=center>給　料<br>（1回出勤）</td><td rowspan=2 align=center>ボーナス</td><td rowspan=2>支払い</td><td rowspan=2 nowrap>身体<br>消費</td><td rowspan=2 nowrap>頭脳<br>消費</td></tr>
	<tr bgcolor=#ffcc33 align=center><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td nowrap>体格指数</td><td nowrap>性別</td><td nowrap>身長</td></tr>
	
	<tr bgcolor=#ffff33 align=center><td>現在の$nameさんのパラメータ</td><td>$kokugo</td><td>$suugaku</td><td>$rika</td><td>$syakai</td><td>$eigo</td><td>$ongaku</td><td>$bijutu</td><td>$looks</td><td>$tairyoku</td><td>$kenkou</td><td>$speed</td><td>$power</td><td>$wanryoku</td><td>$kyakuryoku</td><td>$love</td><td>$unique</td><td>$etti</td><td nowrap>$BMI</td><td>$sex</td><td>$sintyou</td><td align=center nowrap>-</td><td nowrap>-</td><td>-</td><td>-</td><td>-</td></tr>
EOM
	$i=1;
	foreach  (@job_hairetu) {
			&job_sprit($_);
			if ($job_syurui) {if($job_syurui ne $jobsyu){next;}}
			if ($job_BMI_min eq "" && $job_BMI_max eq ""){$BMI_hani = "";}
			elsif ($job_BMI_min eq "" ){$BMI_hani = "$job_BMI_max以下";}
			elsif ($job_BMI_max eq "" ){$BMI_hani = "$job_BMI_min以上";}
			else {$BMI_hani = "$job_BMI_min～$job_BMI_max";}
			
			if ($job_siharai eq "1"){$sihrai_seikei = "日払い";}
			else{$sihrai_seikei = "$job_siharai回出勤ごと";}
			
			if ($job_sintyou){$job_sintyou = "$job_sintyou以上";}
			if($job_sex eq "m") {$job_sex = "男";}elsif($job_sex eq "f"){$job_sex = "女";}
			if($job_rank) {$job_hosi = "*" x ($job_rank-1);}
			
		print <<"EOM";
	<tr bgcolor=#ffcc66 align=center><td nowrap>$job_name$job_hosi</td><td>$job_kokugo</td><td>$job_suugaku</td><td>$job_rika</td><td>$job_syakai</td><td>$job_eigo</td><td>$job_ongaku</td><td>$job_bijutu</td><td>$job_looks</td><td>$job_tairyoku</td><td>$job_kenkou</td><td>$job_speed</td><td>$job_power</td><td>$job_wanryoku</td><td>$job_kyakuryoku</td><td>$job_love</td><td>$job_unique</td><td>$job_etti</td><td nowrap>$BMI_hani</td><td>$job_sex</td><td nowrap>$job_sintyou</td><td align=right nowrap>$job_kyuuyo円</td><td nowrap>×$job_bonus</td><td nowrap>$sihrai_seikei</td><td>$job_energy</td><td>$job_nou_energy</td></tr>
EOM
		if ($i % 10 == 0){print <<"EOM";
	<tr bgcolor=#ff9933 align=center><td nowrap rowspan=2>職業</td><td colspan=17>必要なパラメータ</td><td align=center colspan=3>条　件</td><td rowspan=2 align=center>給　料<br>（1回出勤）</td><td rowspan=2 align=center>ボーナス</td><td rowspan=2>支払い</td><td rowspan=2 nowrap>身体<br>消費</td><td rowspan=2 nowrap>頭脳<br>消費</td></tr>
	<tr bgcolor=#ffcc33 align=center><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td nowrap>体格指数</td><td nowrap>性別</td><td nowrap>身長</td></tr>
	<tr bgcolor=#ffff33 align=center><td>現在の$nameさんのパラメータ</td><td>$kokugo</td><td>$suugaku</td><td>$rika</td><td>$syakai</td><td>$eigo</td><td>$ongaku</td><td>$bijutu</td><td>$looks</td><td>$tairyoku</td><td>$kenkou</td><td>$speed</td><td>$power</td><td>$wanryoku</td><td>$kyakuryoku</td><td>$love</td><td>$unique</td><td>$etti</td><td nowrap>$BMI</td><td>$sex</td><td>$sintyou</td><td align=center nowrap>-</td><td nowrap>-</td><td>-</td><td>-</td><td>-</td></tr>
EOM
		}
		$i ++;
	}
	print <<"EOM";
	</table>
EOM
	&hooter("login_view","戻る");
	exit;
}

#----------職業チェンジ処理----------#
sub job_change_go {
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);

	if ($disp_rireki eq 'yes'){
		$job_keiken_f = "./member/$k_id/job_log.cgi";
		if (-e $job_keiken_f){
			open (IN,"< $job_keiken_f" || &error("ファイルを開くことが出来ませんでした。"));
			eval{ flock (IN, 1); };
			$job_keiken0 = <IN>;
			close(IN);
			chomp $job_keiken0;
		}
	}
	
	$mae_job = $job;
	foreach  (@job_hairetu) {
		&job_sprit($_);
		if($in{'job_sentaku'} eq "$job_no"){
			$job = $job_name;
			$job_keiken = 0;
			$job_kaisuu = 0;
			last;
		}
	}

	if ($disp_rireki eq 'yes'){
		$job_keiken0 .= "$job_name \n";

		open(OUT,">$job_keiken_f") || &error("$job_keiken_fに書き込めません");
		eval{ flock (OUT, 2); };
		print OUT $job_keiken0;
		close(OUT);
	}
	
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	&news_kiroku("就職","$in{'name'}さんが、$mae_job から $job になりました。");
	&message("$job_nameになりました。","login_view");
}

#----------仕事する----------#
sub do_work {
	$date_sec = time;
	unless ($in{'mysec'}){$in{'mysec'} = $date_sec;}
	$jisa = $in{'mysec'} - $date_sec;
	$house_name = $house_name+$jisa;
	($sec_dis,$min_dis,$hour_dis) = localtime($house_name);
	if ($min_dis < 10){$min_dis = '0'.$min_dis}
	if ($sec_dis < 10){$sec_dis = '0'.$sec_dis}
	$shgotonokoritime_m = int((60*$work_seigen_time-($date_sec - $house_name)) / 60);
	$shgotonokoritime_s = (60*$work_seigen_time-($date_sec - $house_name))%60;
	if ($shgotonokoritime_s < 10){$shgotonokoritime_s = '0'.$shgotonokoritime_s}

	if ($date_sec - $house_name < 60*$work_seigen_time){
		&error("仕事できる間隔は$work_seigen_time分です。<br>$in{'mysec'} = $date_sec <br>$hour_dis:$min_dis:$sec_dis 残り $shgotonokoritime_m分$shgotonokoritime_s秒");
	}
	
	open(SP,"< ./dat_dir/job.cgi") || &error("Open Error : ./dat_dir/job.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@job_hairetu = <SP>;
	close(SP);
	foreach  (@job_hairetu) {
			&job_sprit($_);
			if($job_name eq "$job"){
				last;
			}
	}
	
#==========仕事の能力をチェック==========#
	if ($kokugo < $job_kokugo || $suugaku < $job_suugaku || $rika < $job_rika || $syakai < $job_syakai || $eigo < $job_eigo || $ongaku < $job_ongaku || $bijutu < $job_bijutu || $looks < $job_looks || $tairyoku < $job_tairyoku || $kenkou < $job_kenkou || $speed < $job_speed || $power < $job_power || $wanryoku < $job_wanryoku || $kyakuryoku < $job_kyakuryoku || $love < $job_love || $unique < $job_unique || $etti < $job_etti){&error("この仕事に必要な能\力値を下回っているため仕事できません。");}
		#+++++BMIをチェック+++++#
	$taijuu = sprintf ("%.1f",$taijuu);
	&check_BMI($sintyou,$taijuu);
	if($energy < "$job_energy"){&error("身体パワーが足りません！。<br>仕事するには$job_energyの身体パワーが必要です。");}
	if($nou_energy < "$job_nou_energy"){&error("頭脳パワーが足りません！<br>仕事するには$job_nou_energyの頭脳パワーが必要です。");}
	if($job_BMI_min){
			if($BMI < "$job_BMI_min"){&error("体格指数が条件値以下のため仕事できません！");}
	}
	if($job_BMI_max){
			if($BMI > "$job_BMI_max"){&error("体格指数が条件値以上のため仕事できません！");}
	}
		#+++++身体パワー計算+++++#
$energy = $energy + int(($date_sec - $last_ene_time) / $sintai_kaihuku);
$last_ene_time= $date_sec;
$energy_max = int(($tairyoku / 2) + ($kenkou / 3) + ($power / 5) + ($wanryoku / 8) + ($kyakuryoku / 8));
if($energy > $energy_max){$energy = $energy_max;}
if($energy < 0){$energy = 0;}
		#+++++頭脳パワー計算+++++#
$nou_energy = $nou_energy + int(($date_sec - $last_nouene_time) / $zunou_kaihuku);
$last_nouene_time= $date_sec;
$nou_energy_max = int(($kokugo / 4) + ($suugaku / 4) + ($rika / 4) + ($syakai / 4) + ($eigo / 4)+ ($ongaku / 4)+ ($bijutu / 4));
if($nou_energy > $nou_energy_max){$nou_energy = $nou_energy_max;}
if($nou_energy < 0){$nou_energy = 0;}
	
	$mae_job_level = int($job_keiken / 100) ;
	
#==========経験値をプラス==========#
if($in{'cond'} eq "最高") {$randed = "15";}
elsif($in{'cond'} eq "良好") {$randed = "10";}
elsif($in{'cond'} eq "普通") {$randed = "5";}
elsif($in{'cond'} eq "不良") {$randed = "1";}
elsif($in{'cond'} eq "悪い") {$randed = "-5";}
elsif($in{'cond'} eq "<font color=#ff6600>風邪ぎみ</font>") {$randed = "-8";}
elsif($in{'cond'} eq "<font color=#ff6600>風邪</font>") {$randed = "-14";}
elsif($in{'cond'} eq "<font color=#ff6600>下痢</font>") {$randed = "-17";}
elsif($in{'cond'} eq "<font color=#ff6600>肺炎</font>") {$randed = "-20";}
else{&error("その体では仕事できません！");}
	$randed += int(rand(5))+1;
	$job_keiken += $randed;
	
if($randed > 0) {$print_messe .= "・$randedの経験値を得ました。<br>";}
elsif($randed < 0) {$randed *= -1;$print_messe .= "・経験値が$randed減ってしまいました。<br>";}
else{$print_messe .= "・経験値を得ることができませんでした。<br>";}
		#+++++レベルアップ計算、昇給額計算+++++#
	$ato_job_level = int($job_keiken / 100) ;
	$syoukyuugaku = ($job_kyuuyo*$ato_job_level / 100)*$job_syoukyuuritu;
	$job_kyuuyo += $syoukyuugaku;
		#+++++レベルアップ+++++#
	if($ato_job_level > $mae_job_level){
			$print_messe .= "・レベルが上がりました！<br>";
			$print_messe .= "・$job_kyuuyo円／1回に昇給しました。<br>";
			$bonusgaku = $job_kyuuyo * $job_bonus;
			if ($shiharai eq 'yes'){
				$bank += $bonusgaku;
				&kityou_syori("ボーナス","",$bonusgaku,$bank,"普");
			}else{
				$money += $bonusgaku;
			}
		  
			if($bonusgaku > 0){
					$print_messe .= "・$bonusgaku円のボーナスが出ました！<br>";
			}
			if ($ato_job_level >= 15){
				if ($jobsyu ne "$job"){
					$jobsyu = "$job";
					$print_messe .= "・$jobの仕事をマスターしました！<br>";
				}
			}
	}
	
	$job_kaisuu ++;
#==========支払い規定回で割り切れたら給料支給==========#
	if($job_kaisuu % $job_siharai ==0){
			$kyounosiharai = $job_kyuuyo * $job_siharai;
			if ($shiharai eq 'yes'){
				$bank += $kyounosiharai;
				&kityou_syori("給料受取","",$kyounosiharai,$bank,"普");
			}else{
				$money += $kyounosiharai;
			}
			if ($job_siharai == 1){
				$print_messe .= "・$kyounosiharai円の給料をもらいました！<br>";
			}else{
				$print_messe .= "・$kyounosiharai円（$job_kyuuyo円×$job_siharai回出勤）の給料が出ました！<br>";
			}
	}
	
	#+++++エネルギーと体重を減らす+++++#
	$energy -= $job_energy;
	$nou_energy -= $job_nou_energy;
	$taijuu_heri = ($job_energy / 100);
	$taijuu -= $taijuu_heri;
	$print_messe .= "・$taijuu_heri kg体重が減りました。";
		#+++++最後に仕事した時間を記録+++++#
	$house_name = $date_sec;

			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
	&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table  border=0  cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●仕事に出かけました（$job_kaisuu回目）<br>
$print_messe
</span>
	<form method=POST action="$script">
次回の給料支払い<br>
EOM

	if ($shiharai eq "yes"){
		print '<input type=radio name=shiharai value="yes" checked>';
	}else{
		print '<input type=radio name=shiharai value="yes">';
	}
	print "銀行振込み<br>\n";

	if ($shiharai eq "no"){
		print '<input type=radio name=shiharai value="no" checked>';
	}else{
		print '<input type=radio name=shiharai value="no">';
	}
	print "現金受け取り<br>\n";

	print <<"EOM";
	<input type=hidden name=mode value="shiharaihouhou">
	<input type=hidden name=mysec value="$in{'mysec'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="決定">
	</form>

</td></tr></table>
<br>

	<form method=POST action="$script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=mysec value="$in{'mysec'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	</body></html>
EOM
exit;
}

#----------人生ゲームに送金----------#
sub zinseisoukin{
	if($in{'sokingaku'} <= 0){&error("０円、マイナスの金額は振り込むことができません");}
	if($in{'sokingaku'} =~ /[^0-9]/){&error("金額は半角数字で記入してください");}
	if ($bank < $in{'sokingaku'}){&error("普通口座に必要なお金が足りません。");}
	if ($in{'sokingaku'} > 1000000){&error("一回に送られる額は1,000,000円までです。");}

	if($zinsei_soukin_seigen eq 'yes' || $zinsei_jougen_soukin eq 'yes'){
		local(@my_tuutyou);
		$ginkoumeisai_file="./member/$k_id/ginkoumeisai.cgi";
		open(GM,"< $ginkoumeisai_file") || &error("自分の預金通帳ファイルが開けません");
		eval{ flock (GM, 1); };
		@my_tuutyou = <GM>;
		close(GM);
		my($sec0,$min0,$hour0,$mday0,$mon0,$year0) = localtime;
		$date_in = sprintf("%04d/%02d/%02d",$year0+1900,$mon0+1,$mday0);
		$jougen = $in{'sokingaku'};
		foreach (@my_tuutyou){
			(@meisai) = split(/<>/);
			if($meisai[0] eq $date_in && $meisai[1] eq '人生送金'){
				if($zinsei_soukin_seigen eq 'yes'){
					&error("人生ゲームには１日１回しか送金出来ません");
					last;
				}
				$jougen += $meisai[2];
				if($jougen > 1000000 && $zinsei_jougen_soukin eq 'yes'){
					&error("人生ゲームには1,000,000しか送金出来ません<br>$jougen送れません");
					last;
				}
			}
		}
	}

	$zinsei_failu = "$dir_zinsei/zinseilog.cgi";
	open(IN,"< $zinsei_failu") || &error("送金先のファイルが開けません1");
	eval{ flock (IN, 1); };
	@zinseilog = <IN>;
	close(IN);
	$name_aru = 0;
	foreach (@zinseilog){
		(@zinseitmp) = split(/<>/);
		if($zinseitmp[1] eq $in{'name'}){
			$name_no = $zinseitmp[0];
			$name_aru = 1;
			last;
		}
	}
	if(!$name_aru){&error("人生ゲームにありません。");}
	$zinsei_kozin_f = "$dir_zinsei/member/$name_no"."log.cgi";
	open(IN,"< $zinsei_kozin_f") || &error("送金先のファイルが開けません2");
	eval{ flock (IN, 1); };
	$zinseikozinlog0 = <IN>;
	@zinseikozinlog1 = <IN>;
	close(IN);

	(@zinsei_kozin) = split(/<>/,$zinseikozinlog0);
	$zinsei_kozin[3] += $in{'sokingaku'};
	$zinseikozinlog0 = join ("<>",@zinsei_kozin);
	open(OUT,">$zinsei_kozin_f") || &error("送金先のファイルが開けません3");
	eval{ flock (OUT, 2); };
	print OUT $zinseikozinlog0;
	print OUT @zinseikozinlog1;
	close(OUT);
	
	$bank -= $in{'sokingaku'};
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
	&kityou_syori("人生送金","$in{'sokingaku'}","","$bank","普");

	&message("人生ゲームに$in{'sokingaku'}円送金しまし$date_kityouた。","login_view");
	exit;
}
