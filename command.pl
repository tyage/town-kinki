#---------------食堂・デパート-------------------#
#今日の食堂メニュー記録ファイル2
$syokudou_logfile2='./log_dir/syokudoulog2.cgi';
# 食堂の更新リミット残り食品品目 0 は全部売り切れの時。
$syokudounokori = 25;
if($syokudounokori >= $syokudou_sinakazu){$syokudounokori = 0;}
#今日のデパート2の品揃え記録ファイル
$depart_logfile2='./log_dir/departlog2.cgi';
# デパート2の卸問屋の指定
$syouhin_dat_fail ='./dat_dir/syouhin.cgi';
# 秘伝商品を作るか　'yes'
$hidensyouhin = 'yes';

#---------------自動販売機-------------------#
# 自動販売機データファイル
$hanbai_detafile = "./dat_dir/jihanki.cgi";
# 自動販売機保存リスト
$hanbai_logfile = "./log_dir/jihanlog.cgi";
# 並べる数
$habaisurukazu = 10;
# 販売更新時間(1～22)の間
$habaikoushin = 12;

#---------------家関連-------------------#
# 持ち家数
$mochiie_max = 5;
# 家追加の値段。
@housu_tuika2 = (100,100,1000,500);
# 二軒目以後の家の倍率
$ie_bairitu = 2;
# 宅地分譲　専用地以外に建てられなくする
$takuthisyubetu = 'no'; # 'yes' or 'no'
# 管理者専用画像　img内の表示させたい画像名。
$kanri_senyou = ''; #'aisatu.gif'
# 基本能力審査
$kihonnoryoku_sinsa = 'yes';# 'yes' or 'no'
# 問屋で仕入れ主の名前を付ける
$shiire_name = 'no';#'yes'
# 自分の住んでいるタウン以外での購入制限　家を持っていない場合は関係なし 'yes'
$no_mytown = 'no'; # 'yes'; #特定の街は除外可能

####################################################
#/////////////////以下サブルーチン/////////////////#
####################################################

#---------------街情報を変数に代入-------------------#
sub town_no_get {
	if (@_[0] eq ""){
#==========街指定が無く名前指定がある場合（ログイン時）自分の家のある街をチェック=============
		if ($in{'name'}){
			open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
			eval{ flock (IN, 1); };
			@ori_ie_para = <IN>;
			close(IN);
			$iearuflag = 0;
			foreach (@ori_ie_para){
					&ori_ie_sprit($_);
					if ($ori_ie_name eq "$in{'name'}"){$this_town_no = $ori_ie_town; $iearuflag=1; last;}
			}
			if ($iearuflag == 0){$this_town_no = 0;}
#==========街指定が無く名前指定も無い場合（トップページへのアクセス）=============
		}else{$this_town_no = 0;}
#==========街指定があればその街のログを開く=============
	}else{
		$this_town_no = @_[0];
	}
	if (! $in{'town_no'}){$in{'town_no'} = "$this_town_no";}
}

#---------------建築-------------------#
sub kentiku {
	&header(kentiku_style);
    
	$i = 21;
	foreach (A..L){
		$tateziku .= "縦軸<option value=$i>$_</option>\n";
		$i += 17;
	}
	foreach (1..16){
		$yokoziku .= "横軸<option value=$_>$_</option>\n";
	}
	
	#=====　表示させたい画像表示　=====#
	if ($in{'pass'} eq "$admin_pass" && $in{'name'} eq "$admin_name" && $kanri_senyou){
		$ie_hash{"$kanri_senyou"} = 0;
	}
	@ie_keys = ();
	@ie_values = ();

	if ($in{'town_no'} eq $tokusyu_ie_no){
		#=====　家画像をハッシュから展開　=====#
		while(($ie_key,$ie_val) = each %ie_hash2){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;
		}
	}else{
		#=====　家画像をハッシュから展開　=====#
		while(($ie_key,$ie_val) = each %ie_hash){
			push @ie_keys,$ie_key;
			push @ie_values,$ie_val;
		}
	}
	@ie_rank = @ie_keys[sort {$ie_values[$a] <=> $ie_values[$b]} 0 .. $#ie_values];
	
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	
	$n =0;
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if ($name eq "$ori_ie_name"){
			$n++;
		}
	}
	
	$i=1;
	if ($in{'town_no'} eq $tokusyu_ie_no && $tokusyu_ie_no ne ''){
		foreach(@ie_rank){
			if ($n != 0){
				$ie_hash{$_} *= $ie_bairitu;
				$ie_nedan = $ie_bairitu;
			}
			$iegazou .= "<td align=center><label><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円</label><br>$name_hash2{$_}\n";
			if ($i % 8 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}else{
		foreach(@ie_rank){
			if ($n != 0){
				$ie_hash{$_} *= $ie_bairitu;
				$ie_nedan = $ie_bairitu;
			}
			$iegazou .= "<td align=center><label><input type=radio name=iegazou value=$_><br><img src=\"$img_dir/$_\" width=32 height=32><br>$ie_hash{$_}万円</label><br>$name_hash{$_}\n";
			if ($i % 8 == 0){$iegazou .= "</tr><tr>";}
			$i ++;
		}
	}
	
	$i=0;
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		if ($name eq "$ori_ie_name"){
			$i++;
		}
	}
	
	#=====　家の内容表示　=====#
	if ($i >= 1){
		if ($kihonnoryoku_sinsa eq 'yes'){
			$i_k=0;
			if ($k_sousisan >= 100000000){$i_k++;}
			if ($kokugo >= 10000){$i_k++;}
			if ($suugaku >= 10000){$i_k++;}
			if ($rika >= 10000){$i_k++;}
			if ($syakai >= 10000){$i_k++;}
			if ($eigo >= 10000){$i_k++;}
			if ($ongaku >= 10000){$i_k++;}
			if ($bijutu >= 10000){$i_k++;}
			if ($looks >= 10000){$i_k++;}
			if ($tairyoku >= 10000){$i_k++;}
			if ($kenkou >= 10000){$i_k++;}
			if ($speed >= 10000){$i_k++;}
			if ($power >= 10000){$i_k++;}
			if ($wanryoku >= 10000){$i_k++;}
			if ($kyakuryoku >= 10000){$i_k++;}
			if ($love >= 10000){$i_k++;}
			if ($unique >= 10000){$i_k++;}
			if ($etti >= 10000){$i_k++;}
			if ($i_k >= 18){
				$disp_kaisya = "<input type=radio name=tuika value=\"2\">株式会社：$housu_tuika2[2]万円（株式会社運営）<br>\n";
				$disp_mothi = "<input type=radio name=tuika value=\"3\">持ち物販売店：$housu_tuika2[3]万円（持ち物販売店）<br>\n";
			}else{
				$disp_kaisya = "株式会社設営能\力不足<br>\n";
			}
		}else{
			$disp_kaisya = "<input type=radio name=tuika value=\"2\">株式会社：$housu_tuika2[2]万円（株式会社運営）<br>\n";
			$disp_mothi = "<input type=radio name=tuika value=\"3\">持ち物販売店：$housu_tuika2[3]万円（持ち物販売店）<br>\n";
		}
		$disp_ie_ranku = "<br><div class=honbun2>●建築指定してください（内装費）。</div><br>\n";
		
		foreach (@ori_ie_para){
			&ori_ie_sprit($_);
			($ie,$kuwake) = split(/\_/,$ori_k_id);
			if ($k_id eq $ie){
				if ($kuwake eq "0"){$ie0_f = 1;}
				elsif ($kuwake eq "1"){$ie1_f = 1;}
				elsif ($kuwake eq "2"){$ie2_f = 1;}
				elsif ($kuwake eq "3"){$ie3_f = 1;}
			}
		}
		
		unless ($ie0_f){
			$disp_ie_ranku .= "<input type=radio name=tuika value=\"0\">家のみ：$housu_tuika2[0]万円（家のみの表\示）<br>\n";
		}
		unless ($ie1_f){
			$disp_ie_ranku .= "<input type=radio name=tuika value=\"1\">運営：$housu_tuika2[1]万円（運営作業を行う）<br>\n";
		}
		unless ($ie2_f){
			$disp_ie_ranku .= "$disp_kaisya";
		}
		unless ($ie3_f){
			$disp_ie_ranku .= "$disp_mothi";
		}
		
	}else{
		$disp_ie_ranku = <<"EOM";
<br><div class=honbun2>●家のランクを指定してください（内装費）。</div><br>
<input type=radio name=matirank value="0">Ａランク：$housu_nedan[0]万円（４コンテンツ同時表\示が可能\）<br>
<input type=radio name=matirank value="1">Ｂランク：$housu_nedan[1]万円（３コンテンツ同時表\示が可能\）<br>
<input type=radio name=matirank value="2">Ｃランク：$housu_nedan[2]万円（２コンテンツ同時表\示が可能\）<br>
<input type=radio name=matirank value="3">Ｄランク：$housu_nedan[3]万円（１コンテンツ同時表\示が可能\）<br><br>
※自分の家を建てると以下のコンテンツを家の中に設置することができます。<br><br>
<font color=#ff6600>○簡易掲示板</font>：家主はもちろん家を訪れた人が誰でも書き込みできる掲示板です。<br>
<font color=#ff6600>○商売スペース</font>：自分の好きな商品を卸問屋から仕入れ、自由に価格を設定して販売することができます（将来的にはスクールやスポーツジムなど他の商売を開くことも可能\になる予\定です）。<br>
<font color=#ff6600>○独自URLスペース</font>：自分の好きなURLを指定してIFRAMEウインドウに表\示することができます。アイディア次第で自分の家をどんな内容にすることも可能\なので、自分のホームページをお持ちの方にはお奨めです。<br>
<font color=#ff6600>○家主掲示板</font>：管理者のみが書き込みできる掲示板です。日記やエッセイなど自分の文章を表\現したい方にお奨めです。<br><br>
Dランクでは上記コンテンツよりひとつだけ選んで設置することができ、Aランクでは全てのコンテンツを設置できることになります。<br>また、全ての家には「さい銭箱」が置かれていて訪問者の方が自由にさい銭することができます。
EOM
	}
	
	print <<"EOM";
<table width="90%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
<tr>
<td bgcolor=#ffffff>空き地スペースであれば好きな街の好きな場所に自分の家を建てることができます。<br>
建築費用は「その街の地価」＋「家の値段（外装費）」＋「内装費（ランクA～D）」です。家を持つと、以後ログイン時に最初にその街へ行くことになります。</td>
<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>建　築</b></font></td>
</tr></table><br>
<form method="POST" action="$script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>kentiku_do<>">
<input type=hidden name=command value="kakunin">
<input type=hidden name=ie_nedan value ="$ie_nedan">
<table width="80%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
<tr><td valign=top>
<div class=honbun2>●建てる場所を指定してください。家は１軒目<img src=$img_dir/akiti.gif width=32 height=32>２軒目<img src=$img_dir/akiti3.gif width=32 height=32>の場所にのみ建てることができます。</div><br>
<input type="hidden" name="mati_sentaku" value="$in{'town_no'}">
縦軸 <select name="tateziku">$tateziku</select>
横軸 <select name="yokoziku">$yokoziku</select><br>
▼場所がわからない場合、<a href=$script?town_no=$in{'town_no'} target=_blank><u>ここ</u></a>をクリックして確認してください。<br>
<br><br>
<div class=honbun2>●家の選択</div>
<table boader=0 cellspacing="0" cellpadding="5" width=100%><tr>
$iegazou
</tr></table>
</td></tr><tr><td>
$disp_ie_ranku
<br><br><div align="center"><input type=submit value=" 確認画面へ "></div>
</td></tr></table>
<div align="center"><a href=\"javascript:history.back()\"> [前の画面に戻る] </a></div>
</body></html>
EOM
	exit;
}

#=====　施工作業　=====#
sub kentiku_do {
	#=====　確認画面出力　=====#
	if ($in{'command'} eq "kakunin"){
		&main_view($in{'mati_sentaku'});
		exit;
	}
	if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
		if ($in{'siharaihouhou'} ne "現金"){
			if($bank - $in{'kensetu_hiyou'} * 10000 < 0){&error("貯金がありません。");}
		}else{
			if ($in{'kensetu_hiyou'} * 10000 > $money){&error("お金が足りません。");}
		}
	}
	&lock;
	
	#=====　家リストへの書き込み　=====#
	open(IN,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (IN, 1); };
	@ori_ie_para = <IN>;
	close(IN);
	
	$i=0;
	foreach (@ori_ie_para){
		&ori_ie_sprit($_);
		($ori_k_id_0,$ori_k_no) = split(/\_/, $ori_k_id);
		if ($in{'ori_k_id'} eq "$ori_k_id_0"){
			++$i;
			if ($i > $mochiie_max - 1){
				$disp_ie = $i + 1;
				&error("家は一人$mochiie_max軒しか建てられません。引っ越しの場合は、家管理画面から家を売却したのち新たに購入してください。");
			}
		}
	}
	
	&time_get;
	if($in{'ori_ie_tuika'} eq ""){
		$disp_ie = "『$in{'name'}』の家";
		$ie_nomal_flag = 1;
	}elsif($in{'ori_ie_tuika'} eq "0"){
		$disp_ie = "『$in{'name'}』の支店";
	}elsif($in{'ori_ie_tuika'} eq "1"){
		$disp_ie = "『$in{'name'}』の運営会社";
	}elsif($in{'ori_ie_tuika'} eq "2"){
		$disp_ie = "『$in{'name'}』の株式会社";
	}elsif($in{'ori_ie_tuika'} eq "3"){
		$disp_ie = "『$in{'name'}』の持ち物販売店";
	}
	
	if(!$ie_nomal_flag){$in{'ori_k_id'} = "$in{'ori_k_id'}".'_'."$in{'ori_ie_tuika'}";}
	$ori_ie_temp = "$in{'ori_k_id'}<>$in{'name'}<>$disp_ie<>$in{'ori_ie_image'}<><>$date_sec<>$in{'town_no'}<>$in{'ori_ie_tateziku'}<>$in{'ori_ie_yokoziku'}<>$in{'ori_ie_sentaku_point'}<>$in{'ori_ie_tuika'}<><><><><>\n";
	
	push (@ori_ie_para,$ori_ie_temp);
	
	#=====　タウン情報に書き込み　=====#
	if(!$ie_nomal_flag){
		$unei_file="./member/$k_id/$in{'ori_ie_tuika'}"."_log.cgi";
		if (! -e "$unei_file"){
			$all_unei ="1<>$name<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>$in{'ori_ie_tuika'}<>\n";
			open(UNEI,"> $unei_file") || &error("Open Error : $unei_file");
			eval{ flock (UNEI, 2); };
			print UNEI $all_unei;
			close(UNEI);
		}
		
		if ($in{'ori_ie_tuika'} == 2){
			$kin_time = time;
			if (! -e "./member/$k_id/kaishiya_kanri.cgi"){
				open (KAISYA,"> ./member/$k_id/kaishiya_kanri.cgi") || &error("Open Error : ./member/$k_id/kaishiya_kanri.cgi");
				eval{ flock (KAISYA, 2); };
				print KAISYA "$k_id<>$name<>$pass<>$kin_time<>\n";
				close(KAISYA);
			}
			if (! -e "./member/$k_id/kaishiya_bbs.cgi"){
				open (KAISYA,"> ./member/$k_id/kaishiya_bbs.cgi") || &error("Open Error : ./member/$k_id/kaishiya_bbs.cgi");
				eval{ flock (KAISYA, 2); };
				print KAISYA "0<>0<>$k_id<>$name<>$pass<>$kin_time<>\n";
				close(KAISYA);
			}
		}
	}
	
	$write_town_data = "./log_dir/townlog".$in{'town_no'}.".cgi";
	open(TWI,"< $write_town_data") || &error("Open Error : $write_town_data");
	eval{ flock (TWI, 1); };
	$hyouzi_town_hairetu = <TWI>;
	close(TWI);
	@town_sprit_matrix = split(/<>/,$hyouzi_town_hairetu);
	
	($town_sprit_matrix[$in{'ori_ie_sentaku_point'}],$akichi) = split(/=/, $town_sprit_matrix[$in{'ori_ie_sentaku_point'}]);
	if ($takuthisyubetu eq 'yes'){
		if (($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地" || $town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地2") && $i){&error("選択した場所は商業用空き地ではありません。または他の方が既に購入してしまったようです。");
		}elsif(($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地3" || $town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地4") && !$i){&error("選択した場所は住宅用空き地ではありません。または他の方が既に購入してしまったようです。");}
	}else{
		if(!($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地" || $town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地2" || $town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地3" || $town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地4")){&error("選択した場所は空き地ではありません。または他の方が既に購入してしまったようです。");}
	}
	
	if($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地"){$in{'ori_k_id'} = "$in{'ori_k_id'}=空地";}
	if($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地2"){$in{'ori_k_id'} = "$in{'ori_k_id'}=空地2";}
	if($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地3"){$in{'ori_k_id'} = "$in{'ori_k_id'}=空地3";}
	if($town_sprit_matrix[$in{'ori_ie_sentaku_point'}] eq "空地4"){$in{'ori_k_id'} = "$in{'ori_k_id'}=空地4";}
	
	$town_sprit_matrix[$in{'ori_ie_sentaku_point'}] = "$in{'ori_k_id'}";
	$town_temp=join("<>",@town_sprit_matrix);
	
	#=====　タウン情報更新　=====#
	open(TWO,">$write_town_data") || &error("$write_town_dataに書き込めません");
	eval{ flock (TWO, 2); };
	print TWO $town_temp;
	close(TWO);

	#=====　家リスト更新　=====#
	$i=0;
	$nijyuu = 0;
	foreach (@ori_ie_para){
		if ($_ eq $ori_ie_para[0] && $i){
			$nijyuu = $i;
			&error("二重書き込み com 1");
			last;
		}
		$i++;
	}
	if ($nijyuu){
		splice @ori_ie_para,$nijyuu;
	}

	open(OIO,">$ori_ie_list") || &error("$ori_ie_listに書き込めません");
	eval{ flock (OIO, 2); };
	print OIO @ori_ie_para;
	close(OIO);
	
	#=====　ニュース記録　=====#
	if($machikakushi eq 'yes'){
		unless(($town_hairetu[$in{'town_no'}] eq $kakushimachi_name && $kakushimachi_name) || ($town_hairetu[$in{'town_no'}] eq $kakushimachi_name1 && $kakushimachi_name1) || ($town_hairetu[$in{'town_no'}] eq $kakushimachi_name2 && $kakushimachi_name2) || ($town_hairetu[$in{'town_no'}] eq $kakushimachi_name3 && $kakushimachi_name3) || ($town_hairetu[$in{'town_no'}] eq $kakushimachi_name4 && $kakushimachi_name4)){
			&news_kiroku("家","$in{'name'}さんが「$town_hairetu[$in{'town_no'}]」に家を建築しました。");
		}
	}else{
		&news_kiroku("家","$in{'name'}さんが「$town_hairetu[$in{'town_no'}]」に家を建築しました。");
	}
	&unlock;
	
	#=====　ログ更新　=====#
	if ($in{'pass'} ne "$admin_pass" || $in{'name'} ne "$admin_name"){
		if ($in{'siharaihouhou'} ne "現金"){
			$bank -= $in{'kensetu_hiyou'} * 10000;
			&kityou_syori("クレジット支払い（家）","$in{'kensetu_hiyou'}","",$bank,"普");
		}else{
			$money -= $in{'kensetu_hiyou'} * 10000;
		}
	}
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
	&header("","sonomati");
	print <<"EOM";
<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
おめでとうございます！<br>
$town_hairetu[$in{'town_no'}]に家を建築いたしました。<br>
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


######卸問屋
sub orosi {
	open(IN,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 1); };
	$maintown_para = <IN>;
	&main_town_sprit($maintown_para);
	close(IN);
	if($mt_orosiflag == 0){
		&time_get;
##卸フラグが０で規定時間を過ぎていたら
		if($return_hour >= "$mt_t_time"){
			&lock;
#卸フラグを１にしてメインタウンログを更新
			$mt_orosiflag = 1;
			$mt_yobi9 = $date2;		#卸更新日時を記録
			&main_town_temp;
			open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
			eval{ flock (OUT, 2); };
			print OUT $mt_temp;
			close(OUT);	
#商品データログを開く
			open(OL,"< ./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
			eval{ flock (OL, 1); };
			$top_koumoku = <OL>;
#商品をランダムに並び替えてログを更新
			@new_syouhin_hairetu = ();
			@new_syouhin_hairetu2 = (); #koko2006/11/21
		#	srand ($$ | time); #2006/12/19 停止

			while (<OL>){
				my $r = rand @new_syouhin_hairetu+1;
				push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
				$new_syouhin_hairetu[$r] = $_;
			}
			close(OL);
			$i=0;
			foreach (@new_syouhin_hairetu){
				&syouhin_sprit($_);
				if ($syo_syubetu eq "食"){next;}
				if ($syo_syubetu eq 'デパート'){next;}#koko2006/11/21
				$syo_zaiko = int ($syo_zaiko * $ton_zaiko_tyousei); 
				&syouhin_temp;
				push (@new_syouhin_hairetu2,$syo_temp);
				$i ++;
				if ($i >= $orosi_sinakazu){last;}
			}
	
#種別でソートkoko2006/03/12
#			foreach (@new_syouhin_hairetu2){
#				$data=$_;
#				$key=(split(/<>/,$data))[0];
#				push @alldata,$data;
#				push @keys,$key;
#			}

			@alldata = @new_syouhin_hairetu2;
			@keys0 = map {(split /<>/)[0]} @alldata;
			@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];

#			sub by_syu_keys{$keys[$a] cmp $keys[$b];}
#			@alldata=@alldata[ sort by_syu_keys 0..$#alldata]; 
#kokoend2006/03/06	
			open(OLOUT,">$orosi_logfile") || &error("$orosi_logfileに書き込みが出来ません");
			eval{ flock (OLOUT, 2); };
			print OLOUT @alldata;
			close(OLOUT);
	
			&unlock;
		}		#if（商品入れ替え時間が過ぎていた場合）の閉じ
	}		#if（卸フラグが0の場合）の閉じ

#卸商品の表示
	open(IN,"< $orosi_logfile") || &error("Open Error : $orosi_logfile");
	eval{ flock (IN, 1); };
	@kyouno_hairetu = <IN>;
	close(IN);
	&header(orosi_style);
#ver.1.3ここから
#個人の家情報をunitハッシュに代入
	open(OI,"< $ori_ie_list") || &error("Open Error : $ori_ie_list");
	eval{ flock (OI, 1); };
	@ori_ie_hairetu = <OI>;
	foreach (@ori_ie_hairetu) {
			&ori_ie_sprit($_);
			$unit{"$ori_k_id"} = "1";
	}
	close(OI);
	if ($in{'iesettei_id'} eq $k_id){
		&my_omise_orosi_rou;
	}elsif ($in{'iesettei_id'} eq $house_type && $house_type != ""){
		&haiguusya_omise_orosi_rou;
	}else{
		if ($unit{"$k_id"} != ""){
			&my_omise_orosi_rou;
			$in{'iesettei_id'} = $k_id;
		}elsif($unit{"$house_type"} != ""){
			&haiguusya_omise_orosi_rou;
			$in{'iesettei_id'} = $house_type;
		}else{
			$orosisakinomise = "お店を持っていないので仕入れはできません。";
			$settei_t_color = "#888888";
			$misearuyoflag = "nasi";
		}
	}
	
sub my_omise_orosi_rou {
		$orosisakinomise = "自分のお店の仕入れをします。";
		$settei_t_color = "#336699";
		if ($unit{"$house_type"} != ""){
			$change_form = "<form method=POST action=\"$script\"><input type=hidden name=mode value=\"orosi\"><input type=hidden name=iesettei_id value=\"$house_type\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"配偶者のお店の仕入れをする\"></form>";
		}
}

sub haiguusya_omise_orosi_rou {
		$orosisakinomise = "配偶者のお店の仕入れをします。";
		$settei_t_color = "#ff6666";
		if ($unit{"$k_id"} != ""){
			$change_form = "<form method=POST action=\"$script\"><input type=hidden name=mode value=\"orosi\"><input type=hidden name=iesettei_id value=\"$k_id\"><input type=hidden name=name value=\"$in{'name'}\"><input type=hidden name=pass value=\"$in{'pass'}\"><input type=hidden name=town_no value=\"$in{'town_no'}\"><input type=submit value=\"自分のお店の仕入れをする\"></form>";
		}
}

#自分の商品在庫チェック
	$omise_log_file="./member/$in{'iesettei_id'}/omise_log.cgi";
	open(MKF,"< $omise_log_file");
	eval{ flock (MKF, 1); };
	@my_item_list = <MKF>;
	close(MKF);
	foreach (@my_item_list){
		&syouhin_sprit($_);
		($name_temp,$syo_hinmoku) = split(/さんの/, $syo_hinmoku); #koko2007/09/24
		if(!$syo_hinmoku){$syo_hinmoku = $name_temp;} #koko2007/09/24
		$my_omise_zaiko_itiran .= "○$syo_hinmoku $syo_zaiko個　";
	}
#ver.1.3ここまで
#ver.1.30ここから
#2006/11/30 場所移動
	print <<"EOM";

	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>自分のお店に並べる商品をここで仕入れることができます（お店を持ってない方は購入しても意味がありません）。購入したい商品にチェックを入れたうえで、ページ最下部で数量を指定し「OK」ボタンを押してください。品揃えは毎日１回変わりますが、何時に変わるかはランダムに変わります。また、お金は普通口座より引き落とされます。
	<div class=honbun2>最終卸商品更新日時：$mt_yobi9</div>
	<font color=#ff6600>※持っているお店で扱っている種類の商品しか購入できません。スーパーを選択している方は、ここに表\示されている価格の1.5倍になります。<br>
	※お店に置ける商品アイテム数は$mise_zaiko_gendoです。<br>
	※ストックできる一つの商品の在庫数は$mise_zaiko_limitです。</font></td>
	<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>卸　問　屋</b></font></td>
	</tr></table><br>
	<!--ver.1.3ここから-->
	<table width="90%" border="0" cellspacing="0" cellpadding="8" align=center class=yosumi>
	<tr bgcolor=$settei_t_color><td>
	<div align=center style="color:#ffffff;font-size:13px;">$orosisakinomise</div>
	<div align=left style="color:#ffffff;font-size:10px;">現在の在庫状況：$my_omise_zaiko_itiran</div>
	</td>
	<td>$change_form</td>
	</tr></table><br>
	<!--ver.1.3ここまで -->
EOM
	print "<table width=\"100%\" border=\"0\" align=center class=yosumi><tr><td>";#koko2007/03/20
	$subetu = -1;
	foreach (@kyouno_hairetu){
		&syouhin_sprit($_);
		if ($maeno_syo_syubetu ne "$syo_syubetu"){
			$subetu++;
			$maeno_syo_syubetu = $syo_syubetu;
			print "<a href=\"\#s_$subetu\">●$maeno_syo_syubetu</a> ";
		}
	}
	print "</td></tr></table><br>"; #<a name=\"\#s_$subetu\"></a>
#kokoend
	print <<"EOM";
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=27><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br>
	※耐久は、○○回なら使用できる回数、○○日なら使用できる日数です。</font></td></tr>

	<div align=center><form method=POST action="$yobidasi_script">
	<input type=hidden name=mode value="login_view">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}"> <!--ver.1.3-->
	$yobidasi_adminnnnnnnnnnnnnnnnn <!- koko2006/05/30 -->
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="戻る">
	</form></div>

	<form method="POST" action="$script">
	<input type=hidden name=mode value="buy_orosi">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">

EOM
#kokoend

	$subetu = 0;#koko2006/12/01

	foreach (@kyouno_hairetu){
		&syouhin_sprit($_);
			if($syo_zaiko <= 0){
					$syo_zaiko = "売り切れ";
					$kounyuubotan = "";
			}else{
					if ($misearuyoflag eq "nasi"){
						$syo_zaiko = "購入不可";
						$kounyuubotan = "";
					}else{
						$kounyuubotan = "<input type=radio name=syo_hinmoku value=\"$syo_hinmoku,&,$syo_nedan,&,$syo_zaiko,&,$syo_syubetu,&,$syo_syubetu,&,\">"; #koko2006/08/22
					}
			}
			if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "ー";}
			if ($maeno_syo_syubetu ne "$syo_syubetu"){
#koko2006/11/30 #2006/12/01
				if ($kesu){
					$subetu++;
				}else{$kesu = 1;}


				print <<"EOM";
<tr><td align=center colspan=27>購入数(優先$subetu) <input type=\"text\" name=\"kounyuusuu$subetu\" size=10> <input type=submit value="OK"></td></tr>
<tr bgcolor=#cc9966><td align=center width=170><a name="\#s_$subetu"></a>▼$syo_syubetu</td><td align=center nowrap>在庫</td><td align=center>価格</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center nowrap>耐久</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td></tr><!-- #koko2006/11/08 -->
EOM
			}
			$taikyuu_hyouzi_seikei = "$syo_taikyuu"."$syo_taikyuu_tani";
#koko2006/11/08
	if ($syo_comment){
		$disp_seru = "rowspan=\"2\"";
		$disp_com = "<tr bgcolor=#cccccc><td align=left colspan=24>【 備考 】 $syo_comment</td></tr>";
	}else{
		$disp_seru = "";
		$disp_com = "";
	}
#koko2006/12/02
	foreach (@my_item_list){
		(@may_syo) = split(/<>/);
		($name_temp,$may_syo_item) = split(/さんの/, $may_syo[1]); #koko2007/09/24
		if(!$may_syo_item){$may_syo_item = $name_temp;} #koko2007/09/24
		if($syo_syubetu eq $may_syo[0] && $syo_hinmoku eq $may_syo_item){
			$syo_hinmoku = "<font color=\"#ff0000\">$syo_hinmoku $may_syo[24]</font>";
			last;
		}
	}
#kokoend

		print <<"EOM";
	<tr bgcolor=#cccc99><td align=left $disp_seru>$kounyuubotan$syo_hinmoku</td><td align=right nowrap>$syo_zaiko</td><td align=right nowrap>$syo_nedan円</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
#kokoend
		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
	$subetu++;
	if ($misearuyoflag ne "nasi"){
		print <<"EOM";
	<tr><td align=center colspan=27>購入数(優先$subetu) <input type=\"text\" name=\"kounyuusuu$subetu\" size=10> 
<input type=hidden name=subetu value="$subetu">
<input type=submit value="OK"></td></tr>
	</table></form>
EOM
	}else{print "</table></form>";}		#ver.1.40
#ver.1.30ここまで
	&hooter("login_view","戻る");
	exit;
}

#####卸商品購入処理
sub buy_orosi {
#koko2006/12/01
	$i = 0;
	for (0 .. $in{'subetu'}){
		++$loopck;if($loopck > 50){&error("ループオーバーです。$in{'subetu'}");}
		$konuu_tmp = "kounyuusuu$i";#$in{"kounyuusuu15"}=1;
		if ($in{"$konuu_tmp"} > 0){
			$in{'kounyuusuu'} = $in{"$konuu_tmp"};
		}
		$i++;
	}
#kokoend
	if ($in{'kounyuusuu'} < 1){&error("購入数が不適切です。");}
	if($in{'kounyuusuu'} =~ /[^0-9]/){&error("購入数は半角数字で記入してください");}
	($katta_syouhin,$katta_nedan,$imano_zaiko,$orosi_syubetu) = split(/,&,/,$in{'syo_hinmoku'});#koko同一商品の別扱い
#koko2006/10/22
	($name_temp,$katta_syouhin) = split(/さんの/, $katta_syouhin); #koko2007/09/24
	if (!$katta_syouhin){$katta_syouhin = $name_temp;} #koko2007/09/24
	$katta_syouhin_tmp = $katta_syouhin;
	if ($shiire_name eq 'yes'){#koko2007/12/14
		$katta_syouhin = "$in{'name'}さんの$katta_syouhin";

		foreach $syo_tmp(@shiirename){
			if ($katta_syouhin eq $syo_tmp){$katta_syouhin = "$in{'name'}の$syo_tmp";last;}
		}
	}
#end2007/10/19
	if ($katta_syouhin eq '豚'){$katta_syouhin = "$in{'name'}直販の豚";} #koko2007/09/24
#kokoend
	if ($in{'kounyuusuu'} > $imano_zaiko){&error("そんなに在庫がありません1");}
	if ($in{'kounyuusuu'} > $mise_zaiko_limit){&error("お店に置ける在庫の上限は$mise_zaiko_limitです。");}
	open(IN,"< $orosi_logfile") || &error("Open Error : $orosi_logfile");
	eval{ flock (IN, 1); };
		@kyouno_hairetu = <IN>;
	close(IN);
	foreach (@kyouno_hairetu){
		&syouhin_sprit($_);
			if($katta_syouhin eq "$syo_hinmoku"){#koko同一商品の別扱い
				if($syo_zaiko <= 0){&error("在庫がありません2");}
			}
	}
	$katta_total_gaku = $katta_nedan * $in{'kounyuusuu'};
	if ($katta_total_gaku > $bank){&error("普通口座にお金が足りません");}
#自分のお店の種別をチェック
	$omise_settei_file="./member/$in{'iesettei_id'}/omise_ini.cgi";
		open(OIB,"< $omise_settei_file") || &error("お店設定ファイルが開けません。家でお店を開いているか確認してください");
		eval{ flock (OIB, 1); };
			$omise_settei_data = <OIB>;
			($omise_title,$omise_come,$omise_body_style,$omise_syubetu)= split(/<>/,$omise_settei_data);
		close(OIB);
		if ($omise_syubetu ne "スーパー"){
			if ($omise_syubetu ne "$orosi_syubetu"){&error("あなたのお店ではこの商品を扱うことはできません");}
		}
		if ($omise_syubetu eq "スーパー"){
			$katta_nedan *= 1.5;
			$katta_total_gaku *= 1.5;
		}
		
#自分の商品在庫ファイルにその商品があるかチェック
	$omise_log_file="./member/$in{'iesettei_id'}/omise_log.cgi";
	open(MKF,"< $omise_log_file") || &error("自分の商品在庫ファイルが開けません");
	eval{ flock (MKF, 1); };
	@my_item_list = <MKF>;
	close(MKF);
	$motteru_flag =0;
	$my_mise_zaiko = 0;
	@new_myitem_list =(); #koko2007/06/05
#持っているかの判別（持っていたら在庫プラス）と商品アイテム数のカウント
	foreach (@my_item_list){
		&syouhin_sprit($_);
#持っていた場合
		if ($katta_syouhin eq "$syo_hinmoku"){ #koko同一商品の別扱い
			if($omise_syubetu eq "スーパー" && $syo_comment =~ /専門店限定商品/){&error("この商品は$orosi_syubetu専門店でしか購入できません。");}	#ver.1.30
#koko2006/11/21
			if ($omise_syubetu eq "スーパー" && $hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/ && $syo_syubetu ne "スーパー"){
				&error("この秘伝商品は$orosi_syubetu専門店でしか購入できません。");
			}
#kokoend
			$syo_kanou_zaiko = $mise_zaiko_limit - $syo_zaiko;#koko2005/04/17
			$syo_zaiko += $in{'kounyuusuu'};
			if ($syo_zaiko > $mise_zaiko_limit){&error("$katta_syouhinは<br>お店に置ける在庫の上限は$mise_zaiko_limitです。<br>残り $syo_kanou_zaiko個　購入出来ます。");}	#ver.1.3 koko2005/04/17
			$bank -= $katta_total_gaku;
			$motteru_flag =1;
		}
		if ($syo_zaiko <= 0) {next;}
#koko2006/10/22
		($name_temp,$syo_hinmoku) = split(/さんの/, $syo_hinmoku); #koko2007/09/24
		if (!$syo_hinmoku){$syo_hinmoku = $name_temp;} #koko2007/09/24
		if ($shiire_name eq 'yes'){ #2007/12/14
			$syo_hinmoku = "$in{'name'}さんの$syo_hinmoku"; #koko2007/09/24
#koko2007/10/19
			foreach $syo_tmp(@shiirename){
				if ($katta_syouhin eq $syo_tmp){$katta_syouhin = "$in{'name'}の$syo_tmp";last;}
			}
		}
#end2007/10/19
		if ($syo_hinmoku eq '豚'){$syo_hinmoku = "$in{'name'}直販の豚";}

#kokoend
		&syouhin_temp;
		$my_mise_zaiko ++;
		push (@new_myitem_list,$syo_temp);
	}		#foreachの閉じ
#アイテム種類が限度以上なら同じアイテムでも買えない処理
	if($douitem_ok == 1){
		if ($my_mise_zaiko >= $mise_zaiko_gendo){&error("お店に置ける商品アイテム数（$mise_zaiko_gendo）を超えているためまだ仕入れができません。");}
	}
#持っていなかった場合（卸しログファイルよりパラメータごとコピー）
#koko2006/10/22
	$katta_syouhin = $katta_syouhin_tmp;
#kokoend
	if ($motteru_flag ==0){
		if ($my_mise_zaiko >= $mise_zaiko_gendo){&error("お店に置ける商品アイテム数は$mise_zaiko_gendoです。");}
		open(SP,"< $orosi_logfile") || &error("Open Error : $orosi_logfile");
		eval{ flock (SP, 1); };
		@kounyuu_hairetu = <SP>;
		close(SP);
		$kounyuu_ok = 0;
#		@new_myitem_list = (); #koko2007/06/05 #kokohenkou
		foreach (@kounyuu_hairetu){
			&syouhin_sprit($_);
			if ($katta_syouhin eq "$syo_hinmoku"){#koko同一商品の別扱い
			if($omise_syubetu eq "スーパー" && $syo_comment =~ /専門店限定商品/){&error("この商品は$orosi_syubetu専門店でしか購入できません。");}		#ver.1.30
#koko2006/11/21
			if ($omise_syubetu eq "スーパー" && $hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/ && $syo_syubetu ne "スーパー"){
				&error("この秘伝商品は$orosi_syubetu専門店でしか購入できません。");
			}
#kokoend
#購入日を記録
				$syo_kounyuubi = time;
				$syo_zaiko = $in{'kounyuusuu'};
#koko2006/10/22
				($name_temp,$syo_hinmoku) = split(/さんの/, $syo_hinmoku); #koko2007/09/24
				if (!$syo_hinmoku){$syo_hinmoku = $name_temp;} #koko2007/09/24
				if ($shiire_name eq 'yes'){ #koko2007/12/14
					$syo_hinmoku = "$in{'name'}さんの$syo_hinmoku"; #koko2007/09/24
#koko2007/10/19
					foreach $syo_tmp(@shiirename){
						if ($katta_syouhin eq $syo_tmp){$katta_syouhin = "$in{'name'}の$syo_tmp";last;}
					}
				}
#end2007/10/19
				if ($syo_hinmoku eq '豚'){$syo_hinmoku = "$in{'name'}直販の豚";}

#kokoend
				&syouhin_temp;
				push (@new_myitem_list,$syo_temp);
				$bank -= $katta_total_gaku;
				$kounyuu_ok = 1;
				last;
			}
		}
		if ($kounyuu_ok == 0){&error("購入できませんでした。");}
		
	}		#持っていなかった場合の閉じ
	
#ログ更新
			&temp_routin;
			&log_kousin($my_log_file,$k_temp);
#記帳する
			&kityou_syori("仕入れ（$katta_syouhin×$in{'kounyuusuu'}）","$katta_total_gaku","",$bank,"普");
			
#自分の購入物ファイルのログ更新
	&lock;
	open(MK,">$omise_log_file") || &error("自分の商品在庫ファイルに書き込めません");
	eval{ flock (MK, 2); };
	print MK @new_myitem_list;
	close(MK);
	
#卸問屋の残り数を引く
	open(SYO,"< $orosi_logfile") || &error("Open Error : $orosi_logfile");
	eval{ flock (SYO, 1); };
		@depa_zan = <SYO>;
	close(SYO);
	@new_depa_zan=();
	foreach (@depa_zan){
		&syouhin_sprit($_);
		if($katta_syouhin eq "$syo_hinmoku"){#koko同一商品の別扱い
			$syo_zaiko -= $in{'kounyuusuu'} ;
		}
		&syouhin_temp;
		push (@new_depa_zan,$syo_temp);
	}

	open(OLOUT,">$orosi_logfile") || &error("$orosi_logfileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT @new_depa_zan;
	close(OLOUT);

	&unlock;

&header("","sonomati");
	print <<"EOM";
	<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
<span class="job_messe">
●$katta_syouhin（$katta_nedan円×$in{'kounyuusuu'}）を仕入れました（仕入れ総額：$katta_total_gaku円）。
</span>
</td></tr></table>
<br>
	<form method=POST action="$script">
	<input type=hidden name=mode value="orosi">
	<input type=hidden name=iesettei_id value="$in{'iesettei_id'}">		<!--ver.1.3-->
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<input type=submit value="仕入れを続ける">
	</form>
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


#######食堂
sub syokudou {
	#食堂フラグが0ならばメニューを更新、フラグを1にする
	open(IN,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 1); };
	$maintown_para = <IN>;
			&main_town_sprit($maintown_para);
	close(IN);
	if($mt_syokudouflag == 0){
		&lock;
		$mt_syokudouflag = 1;
		&main_town_temp;
		open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
		eval{ flock (OUT, 2); };
		print OUT $mt_temp;
		close(OUT);	
#商品データログを開く
		open(OL,"< ./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
#		srand ($$ | time);

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu ne "食"){next;}
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $syokudou_sinakazu){last;}
		}
		open(OLOUT,">$syokudou_logfile") || &error("$syokudou_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @new_syouhin_hairetu2;
		close(OLOUT);

		#koko2006/07/16
#商品データログを開く
		open(OL,"< ./dat_dir/syokudou2.cgi") || &error("Open Error : ./dat_dir/syokudou2.cgi");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
		@new_syouhin_hairetu2 = (); #koko2006/07/20
#		srand ($$ | time);

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu ne "食"){next;}
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $syokudou_sinakazu){last;}
		}
		open(OLOUT,">$syokudou_logfile2") || &error("$syokudou_logfile2に書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @new_syouhin_hairetu2;
		close(OLOUT);
		#kokomade2006/07/16

		&unlock;
	}		#if（日付が変わっていたら）の閉じ
		
	open(SP,"< $syokudou_logfile") || &error("Open Error : $syokudou_logfile");
	eval{ flock (SP, 1); };
	@syokudou_hairetu = <SP>;
	close(SP);
	
	&header(syokudou_style);
	print <<"EOM";
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr>
	<td colspan=11 bgcolor=#ffffff>セントラル食堂です。メニューは毎日変わります。一度食事をすると$syokuzi_kankaku分経たないと次の食事がとれません。また、$deleteUser日間食事しないと死んでしまいます（ユーザー削除されます）<br></td>
	<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>食　堂</b></font></td>
	</tr>
	<tr><td colspan=14><font color=#336699>凡例：（ル）ルックスup値、（体）体力up値、（健）健康up値、（ス）スピードup値、（パ）パワーup値、（腕）腕力up値、（脚）脚力up値、（L）LOVEup値、（面）面白さup値、（H）エッチup値</font></td></tr>
		<tr bgcolor=#ff9933><td align=center nowrap>メニュー</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center>カロリー</td><td align=center>値段</td><td align=center>残り</td></tr>
EOM
	$nokorisyokuhin = 0; #koko2006/08/26
	$i =1;
	foreach (@syokudou_hairetu) {
		if ($i % 10 ==0){print <<"EOM";
		<tr bgcolor=#ff9933><td align=center nowrap>メニュー</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center>カロリー</td><td align=center>値段</td><td align=center>残り</td></tr>
EOM
		}
		&syouhin_sprit($_);
		$syo_nedan *= 3;
		if($syo_kokugo<=0){$syo_kokugo="";}
		if($syo_suugaku<=0){$syo_suugaku="";}
		if($syo_rika<=0){$syo_rika="";}
		if($syo_syakai<=0){$syo_syakai="";}
		if($syo_eigo<=0){$syo_eigo="";}
		if($syo_ongaku<=0){$syo_ongaku="";}
		if($syo_bijutu<=0){$syo_bijutu="";}
		if($syo_kouka<=0){$syo_kouka="";}
		if($syo_looks<=0){$syo_looks="";}
		if($syo_tairyoku<=0){$syo_tairyoku="";}
		if($syo_kenkou<=0){$syo_kenkou="";}
		if($syo_speed<=0){$syo_speed="";}
		if($syo_power<=0){$syo_power="";}
		if($syo_wanryoku<=0){$syo_wanryoku="";}
		if($syo_kyakuryoku<=0){$syo_kyakuryoku="";}
		if($syo_love<=0){$syo_love="";}
		if($syo_unique<=0){$syo_unique="";}
		if($syo_etti<=0){$syo_etti="";}
		if($syo_zaiko <= 0){
			$kounyuubotan ="";
			$dame ="";
			$syo_zaiko = "売り切れ";
			$dame ="";
		}elsif($money < $syo_nedan*3){
			$kounyuubotan ="";
			$dame ="（お金が足りません。）";
		}else{
			$kounyuubotan ="<input type=submit value=\"食す\">";
			$dame ="";
			$nokorisyokuhin ++;
		}
		print <<"EOM";
		<form method="POST" action="$script" NAME="foMes5">
		<INPUT TYPE="hidden" NAME="TeMes5">
		<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>syokuzisuru<>">
		<input type=hidden value="$syo_hinmoku" name="syo_hinmoku">
		<tr bgcolor="#ffcc66"><td nowrap>$kounyuubotan $syo_hinmoku $dame</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td>$syo_cal kcal</td><td align=right nowrap>$syo_nedan円</td><td align=right>$syo_zaiko</td></tr>
		</form>
EOM
		$i ++;
	}
	print <<"EOM";
	<tr><td colspan=14><div align=center></div></td>
	</table>
EOM
#koko2006/08/26
	if ($nokorisyokuhin <= $syokudounokori){
		$mt_syokudouflag = 0;
		&main_town_temp;
		open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
		eval{ flock (OUT, 2); };
		print OUT $mt_temp;
		close(OUT);
	}
#kokoend2006/08/26
	&hooter("login_view","戻る");

	exit;
}

####食事処理
sub syokuzisuru {		#ver.1.3
	if($in{'syo_hinmoku'} eq ""){&error("食事が選ばれていません");}		#ver.1.40
	open(SP,"< ./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@syokuzi_hairetu = <SP>;
	close(SP);
	foreach $syokuzi_hyouzi (@syokuzi_hairetu) {
		&syouhin_sprit($syokuzi_hyouzi);
		if($in{'syo_hinmoku'} eq "$syo_hinmoku"){
			$now_time = time;
			if($now_time < $last_syokuzi + ($syokuzi_kankaku*60)){&error("まだ食事できません。");}
			if($money < $syo_nedan*3){&error("お金が足りません。");}

#koko2005/04/16
			if($syo_looks){$looks += $syo_looks; $print_messe0 .= "<br>・ルックス値が$syo_looksアップしました。<br>";}
			if($syo_tairyoku){$tairyoku += $syo_tairyoku; $print_messe0 .= "<br>・体力が$syo_tairyokuアップしました。<br>";}
			if($syo_kenkou){$kenkou += $syo_kenkou; $print_messe0 .= "<br>・健康値が$syo_kenkouアップしました。<br>";}
			if($syo_speed){$speed += $syo_speed; $print_messe0 .= "<br>・スピードが$syo_speedアップしました。<br>";}
			if($syo_power){$power += $syo_power; $print_messe0 .= "<br>・パワーが$syo_powerアップしました。<br>";}
			if($syo_wanryoku){$wanryoku += $syo_wanryoku; $print_messe0 .= "<br>・腕力が$syo_wanryokuアップしました。<br>";}
			if($syo_kyakuryoku){$kyakuryoku += $syo_kyakuryoku; $print_messe0 .= "<br>・脚力が$syo_kyakuryokuアップしました。<br>";}
			if($syo_love){$love += $syo_love; $print_messe0 .= "<br>・Loveが$syo_loveアップしました。<br>";}
			if($syo_unique){$unique += $syo_unique; $print_messe0 .= "<br>・面白さが$syo_uniqueアップしました。<br>";}
			if($syo_etti){$etti += $syo_etti; $print_messe0 .= "<br>・エッチ度が$syo_ettiアップしました。<br>";}
			if($syo_cal){$cal_dis = $syo_cal / 1000;$taijuu += $cal_dis; $print_messe0 .= "<br>・体重が$cal_disＫｇアップしました。<br>";}
			if($syo_nedan){$nedan_dis = ($syo_nedan*3); $money -= $nedan_dis; $print_messe0 .= "<br>・お金が$nedan_dis円かかりました。<br>";}

		#	$looks += $syo_looks;
		#	$tairyoku += $syo_tairyoku;
		#	$kenkou += $syo_kenkou;
		#	$speed += $syo_speed;
		#	$power += $syo_power;
		#	$wanryoku += $syo_wanryoku;
		#	$kyakuryoku += $syo_kyakuryoku;
		#	$love += $syo_love;		#ver.1.2
		#	$unique += $syo_unique;		#ver.1.2
		#	$etti += $syo_etti;
		#	$taijuu += $syo_cal / 1000;
			$last_syokuzi = $now_time;
		#	$money -= ($syo_nedan*3);
#kokoend
			last;
		}
	}


#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);
			
#食堂の残り数を引く
	open(SYO,"< $syokudou_logfile") || &error("Open Error : $syokudou_logfile");
	eval{ flock (SYO, 1); };
	@syoku_zan = <SYO>;
	close(SYO);
	@new_syoku_zan=();
	foreach (@syoku_zan){
		&syouhin_sprit($_);
		if($in{'syo_hinmoku'} eq "$syo_hinmoku"){
			$syo_zaiko = $syo_zaiko-1 ;
		}
		&syouhin_temp;
		push (@new_syoku_zan,$syo_temp);
	}
			
	&lock;	
	open(OLOUT,">$syokudou_logfile") || &error("$syokudou_logfileに書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT @new_syoku_zan;
	close(OLOUT);
	&unlock;
	
	&message("$in{'syo_hinmoku'}を食べました。<br>$print_messe0","login_view");#koko2005/04/16
}
#######食堂2 koko2006/07/16
sub syokudou2 {
	#食堂フラグが0ならばメニューを更新、フラグを1にする
	open(IN,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 1); };
	$maintown_para = <IN>;
	&main_town_sprit($maintown_para);
	close(IN);

	if($mt_syokudouflag == 0){
		&lock;
		$mt_syokudouflag = 1;
		&main_town_temp;
		open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
		eval{ flock (OUT, 2); };
		print OUT $mt_temp;
		close(OUT);	
#商品データログを開く
		open(OL,"< ./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
#		srand ($$ | time);

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu ne "食"){next;}
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $syokudou_sinakazu){last;}
		}
		open(OLOUT,">$syokudou_logfile") || &error("$syokudou_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @new_syouhin_hairetu2;
		close(OLOUT);
		#koko2006/07/16
#商品データログを開く
		open(OL,"< ./dat_dir/syokudou2.cgi") || &error("Open Error : ./dat_dir/syokudou2.cgi");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
		@new_syouhin_hairetu2 = (); #koko2006/07/20
#		srand ($$ | time);

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu ne "食"){next;}
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $syokudou_sinakazu){last;}
		}
		open(OLOUT,">$syokudou_logfile2") || &error("$syokudou_logfile2に書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @new_syouhin_hairetu2;
		close(OLOUT);
		#kokomade2006/07/16

		&unlock;
	}		#if（日付が変わっていたら）の閉じ

	open(SP,"< $syokudou_logfile2") || &error("Open Error : $syokudou_logfile2");
	eval{ flock (SP, 1); };

	@syokudou_hairetu = <SP>;
	close(SP);
	&header(syokudou_style);
	print <<"EOM";
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr>
	<td colspan=11 bgcolor=#ffffff>セントラル食堂です。メニューは毎日変わります。一度食事をすると$syokuzi_kankaku分経たないと次の食事がとれません。また、$deleteUser日間食事しないと死んでしまいます（ユーザー削除されます）<br></td>
	<td bgcolor="#333333" align=center width="300"><font color="#ffffff" size="5"><b>食　堂</b></font></td>
	</tr>
	<tr><td colspan=14><font color=#336699>凡例：（ル）ルックスup値、（体）体力up値、（健）健康up値、（ス）スピードup値、（パ）パワーup値、（腕）腕力up値、（脚）脚力up値、（L）LOVEup値、（面）面白さup値、（H）エッチup値</font></td></tr>
		<tr bgcolor=#ff9933><td align=center nowrap>メニュー</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center>カロリー</td><td align=center>値段</td><td align=center>残り</td></tr>
EOM
	$nokorisyokuhin = 0; #koko2006/08/26
	$i =1;
	foreach (@syokudou_hairetu) {
		if ($i % 10 ==0){print <<"EOM";
		<tr bgcolor=#ff9933><td align=center nowrap>メニュー</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center>カロリー</td><td align=center>値段</td><td align=center>残り</td></tr>
EOM
		}
		&syouhin_sprit($_);
		$syo_nedan *= 3;
		if($syo_kokugo<=0){$syo_kokugo="";}
		if($syo_suugaku<=0){$syo_suugaku="";}
		if($syo_rika<=0){$syo_rika="";}
		if($syo_syakai<=0){$syo_syakai="";}
		if($syo_eigo<=0){$syo_eigo="";}
		if($syo_ongaku<=0){$syo_ongaku="";}
		if($syo_bijutu<=0){$syo_bijutu="";}
		if($syo_kouka<=0){$syo_kouka="";}
		if($syo_looks<=0){$syo_looks="";}
		if($syo_tairyoku<=0){$syo_tairyoku="";}
		if($syo_kenkou<=0){$syo_kenkou="";}
		if($syo_speed<=0){$syo_speed="";}
		if($syo_power<=0){$syo_power="";}
		if($syo_wanryoku<=0){$syo_wanryoku="";}
		if($syo_kyakuryoku<=0){$syo_kyakuryoku="";}
		if($syo_love<=0){$syo_love="";}
		if($syo_unique<=0){$syo_unique="";}
		if($syo_etti<=0){$syo_etti="";}
		if($syo_zaiko <= 0){
			$kounyuubotan ="";
			$dame ="";
			$syo_zaiko = "売り切れ";
			$dame ="";
		}elsif($money < $syo_nedan*3){
			$kounyuubotan ="";
			$dame ="（お金が足りません。）";
		}else{
			$kounyuubotan ="<input type=submit value=\"食す\">";
			$dame ="";
			$nokorisyokuhin ++;
		}
		print <<"EOM";
		<form method="POST" action="$script" NAME="foMes5">
		<INPUT TYPE="hidden" NAME="TeMes5">
		<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>syokuzisuru2<>">
		<input type=hidden value="$syo_hinmoku" name="syo_hinmoku">
		<tr bgcolor="#ffcc66"><td nowrap>$kounyuubotan $syo_hinmoku $dame</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td>$syo_cal kcal</td><td align=right nowrap>$syo_nedan円</td><td align=right>$syo_zaiko</td></tr>
		</form>
EOM
		$i ++;
	}
	print <<"EOM";
	<tr><td colspan=14><div align=center></div></td>
	</table>
EOM
#koko2006/08/26
	if ($nokorisyokuhin <= $syokudounokori){
		$mt_syokudouflag = 0;
		&main_town_temp;
		open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
		eval{ flock (OUT, 2); };
		print OUT $mt_temp;
		close(OUT);
	}
#kokoend2006/08/26
	&hooter("login_view","戻る");

	exit;
}

####食事処理2 koko2006/07/16
sub syokuzisuru2 {		#ver.1.3
	if($in{'syo_hinmoku'} eq ""){&error("食事が選ばれていません");}		#ver.1.40
	open(SP,"< ./dat_dir/syokudou2.cgi") || &error("Open Error : ./dat_dir/syokudou2.cgi");
	eval{ flock (SP, 1); };
	$top_koumoku = <SP>;
	@syokuzi_hairetu = <SP>;
	close(SP);
	foreach $syokuzi_hyouzi (@syokuzi_hairetu) {
		&syouhin_sprit($syokuzi_hyouzi);
		if($in{'syo_hinmoku'} eq "$syo_hinmoku"){
			$now_time = time;
			if($now_time < $last_syokuzi + ($syokuzi_kankaku*60)){&error("まだ食事できません。");}
			if($money < $syo_nedan*3){&error("お金が足りません。");}
				
#koko2005/04/16
			if($syo_looks){$looks += $syo_looks; $print_messe0 .= "<br>・ルックス値が$syo_looksアップしました。<br>";}
			if($syo_tairyoku){$tairyoku += $syo_tairyoku; $print_messe0 .= "<br>・体力が$syo_tairyokuアップしました。<br>";}
			if($syo_kenkou){$kenkou += $syo_kenkou; $print_messe0 .= "<br>・健康値が$syo_kenkouアップしました。<br>";}
			if($syo_speed){$speed += $syo_speed; $print_messe0 .= "<br>・スピードが$syo_speedアップしました。<br>";}
			if($syo_power){$power += $syo_power; $print_messe0 .= "<br>・パワーが$syo_powerアップしました。<br>";}
			if($syo_wanryoku){$wanryoku += $syo_wanryoku; $print_messe0 .= "<br>・腕力が$syo_wanryokuアップしました。<br>";}
			if($syo_kyakuryoku){$kyakuryoku += $syo_kyakuryoku; $print_messe0 .= "<br>・脚力が$syo_kyakuryokuアップしました。<br>";}
			if($syo_love){$love += $syo_love; $print_messe0 .= "<br>・Loveが$syo_loveアップしました。<br>";}
			if($syo_unique){$unique += $syo_unique; $print_messe0 .= "<br>・面白さが$syo_uniqueアップしました。<br>";}
			if($syo_etti){$etti += $syo_etti; $print_messe0 .= "<br>・エッチ度が$syo_ettiアップしました。<br>";}
			if($syo_cal){$cal_dis = $syo_cal / 1000;$taijuu += $cal_dis; $print_messe0 .= "<br>・体重が$cal_disＫｇアップしました。<br>";}
			if($syo_nedan){$nedan_dis = ($syo_nedan*3); $money -= $nedan_dis; $print_messe0 .= "<br>・お金が$nedan_dis円かかりました。<br>";}

		#	$looks += $syo_looks;
		#	$tairyoku += $syo_tairyoku;
		#	$kenkou += $syo_kenkou;
		#	$speed += $syo_speed;
		#	$power += $syo_power;
		#	$wanryoku += $syo_wanryoku;
		#	$kyakuryoku += $syo_kyakuryoku;
		#	$love += $syo_love;		#ver.1.2
		#	$unique += $syo_unique;		#ver.1.2
		#	$etti += $syo_etti;
		#	$taijuu += $syo_cal / 1000;
			$last_syokuzi = $now_time;
		#	$money -= ($syo_nedan*3);
#kokoend
			last;
		}
	}


#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

#食堂の残り数を引く
	open(SYO,"< $syokudou_logfile2") || &error("Open Error : $syokudou_logfile2");
	eval{ flock (SYO, 1); };
	@syoku_zan = <SYO>;
	close(SYO);
	@new_syoku_zan=();
	foreach (@syoku_zan){
		&syouhin_sprit($_);
		if($in{'syo_hinmoku'} eq "$syo_hinmoku"){
			$syo_zaiko = $syo_zaiko-1 ;
		}
		&syouhin_temp;
		push (@new_syoku_zan,$syo_temp);
	}

	&lock;	
	open(OLOUT,">$syokudou_logfile2") || &error("$syokudou_logfile2に書き込みが出来ません");
	eval{ flock (OLOUT, 2); };
	print OLOUT @new_syoku_zan;
	close(OLOUT);
	&unlock;

	&message("$in{'syo_hinmoku'}を食べました。<br>$print_messe0","login_view");#koko2005/04/16
}
#######デパート2 #koko2006/11/20
sub depart_gamen2 {
	$departset = 2;
	&depart_gamen;
}
#kokoend
#######デパート
sub depart_gamen {
	#デパートフラグが0ならばメニューを更新、フラグを1にする
	open(IN,"< $maintown_logfile") || &error("Open Error : $maintown_logfile");
	eval{ flock (IN, 1); };
	$maintown_para = <IN>;
	&main_town_sprit($maintown_para);
	close(IN);
	if($mt_departflag == 0){
		&lock;
		$mt_departflag = 1;
		&main_town_temp;
		open(OUT,">$maintown_logfile") || &error("Write Error : $maintown_logfile");
		eval{ flock (OUT, 2); };
		print OUT $mt_temp;
		close(OUT);	
		#商品データログを開く
		open(OL,"< ./dat_dir/syouhin.cgi") || &error("Open Error : ./dat_dir/syouhin.cgi");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
		#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
	#	srand ($$ | time); #koko2006/11/20 消す

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu eq "食"){next;}
#koko2006/11/21
			if ($hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/){next;}
#kokoend
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $depart_sinakazu){last;}
		}
#種別でソートkoko2006/03/12
#		foreach (@new_syouhin_hairetu2){
#			$data=$_;
#			$key=(split(/<>/,$data))[0];
#			push @alldata,$data;
#			push @keys,$key;
#		}

		@alldata = @new_syouhin_hairetu2;
		@keys0 = map {(split /<>/)[0]} @alldata;
		@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];

#		sub by_syu_keys{$keys[$a] cmp $keys[$b];}
#		@alldata=@alldata[ sort by_syu_keys 0..$#alldata]; 
#kokoend2006/03/12	
		open(OLOUT,">$depart_logfile") || &error("$depart_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @alldata;
		close(OLOUT);
#koko2006/11/20
#		&unlock;
# デパート2
		@alldata = ();
		@new_syouhin_hairetu2 = ();

		#商品データログを開く 問屋の指定は上。今は一緒。
		open(OL,"< $syouhin_dat_fail") || &error("Open Error : $syouhin_dat_fail");
		eval{ flock (OL, 1); };
		$top_koumoku = <OL>;
		#商品をランダムに並び替えてログを更新
		@new_syouhin_hairetu = ();
	#	srand ($$ | time);	#koko2006/11/20 消す

		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu eq "食"){next;}
#koko2006/11/21
			if ($hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/){next;}
#kokoend
			$syo_zaiko = int($syo_zaiko / $zaiko_tyousetuti);
			if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $depart_sinakazu){last;}
		}

		@alldata = @new_syouhin_hairetu2;
		@keys0 = map {(split /<>/)[0]} @alldata;
		@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];

		open(OLOUT,">$depart_logfile2") || &error("$depart_logfile2に書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @alldata;
		close(OLOUT);
		&unlock;

	}		#if（日付が変わっていたら）の閉じ

	if ($departset == 2){
		open(SP,"< $depart_logfile2") || &error("Open Error : $depart_logfile2");
		eval{ flock (SP, 1); };
		@syokudou_hairetu = <SP>;
		close(SP);
		$depato_sele = qq|<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>buy_syouhin2<>">|;
		$depa_com = 'デパート２';
#koko2006/11/28
	}elsif($departset == 3){
		open(SP,"< $depart_logfile2") || &error("Open Error : $depart_logfile2");
		eval{ flock (SP, 1); };
		@syokudou_hairetu = <SP>;
		close(SP);
		$depato_sele = qq|<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>buy_syouhin2<>">|;
		$depa_com = '自動販売機';


	}else{
		open(SP,"< $depart_logfile") || &error("Open Error : $depart_logfile");
		eval{ flock (SP, 1); };
		@syokudou_hairetu = <SP>;
		close(SP);
		$depato_sele = qq|<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>buy_syouhin<>">|;
		$depa_com = 'デパート１';
	}

	#選択肢作成
	for ($i=1 ; $i<=$item_kosuuseigen ; $i++){ 
		$kazu_sentaku .= "<option value=\"$i\">$i個</option>";
	}
#koko2006/11/30 場所移動	#所有物チェック
	if(!$k_id){&error("mono.cgi エラー command1")} #koko2007/11/18
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_kounyuu_list =<OUT>;
	close(OUT);
	$kyokasuru = 0; #koko2007/11/04
	foreach (@my_kounyuu_list){
		&syouhin_sprit ($_);
		if ($syo_kouka eq "クレジット"){
			if ($syo_taikyuu - (int ((time - $syo_kounyuubi) / (60*60*24)))){
				$siharai_houhou .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>";
			}
		}
#koko2007/11/04
		if($kyokahin1 && $syo_hinmoku eq $kyokahin1 || $kyokahin2 && $syo_hinmoku eq $kyokahin2){ #koko2007/10/09
			$kyokasuru = 1;
		}elsif($kyokasuru != 1 && ($kyokahin1 || $kyokahin2)){
			$kyokasuru = 2;
		}
#end2007/11/04
	}
	&header(syokudou_style);
	print <<"EOM";
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>$depa_comです。品揃えは毎日変わります。種類は豊富ですが値段は高めです。また一度に持てる所有物の限度は$syoyuu_gendosuu品目です。<div class="honbun2">●$nameさんの所持金：$money円</div></td>
	<td bgcolor=#333333 align=center width="300"><font color="#ffffff" size="5"><b>デパート</b></font></td>
	</tr></table><br>
EOM
	print "<table width=\"100%\" border=\"0\" align=center class=yosumi><tr><td>";#koko2007/03/20
	$subetu = 0;
	foreach (@syokudou_hairetu){
		&syouhin_sprit($_);
		if ($maeno_syo_syubetu ne "$syo_syubetu"){
			$subetu++;
			$maeno_syo_syubetu = $syo_syubetu;
			print "<a href=\"\#s_$subetu\">●$maeno_syo_syubetu</a> ";
		}
	}
	print "</td></tr></table>"; #<a name=\"\#s_$subetu\"></a>#kokoend2007/03/20
	print <<"EOM";
	<table width="100%" border="0" cellspacing="1" cellpadding="5" align=center class=yosumi>
	<tr><td colspan=26><font color=#336699>凡例：(国)＝国語up値、(数)＝数学up値、(理)＝理科up値、(社)＝社会up値、(英)＝英語up値、(音)＝音楽up値、(美)＝美術up値、（ル）=ルックスup値、（体）=体力up値、（健）=健康up値、（ス）=スピードup値、（パ）=パワーup値、（腕）=腕力up値、（脚）=脚力up値、（L）=LOVEup値、（面）=面白さup値、（H）=エッチup値<br></font>
	<font color=#ff6600>※ギフトは贈り物専用の商品です。自分で使用することはできません。</font></td></tr>
	<form method="POST" action="$script">
	$depato_sele
EOM

	$subetu = 0;
	foreach (@syokudou_hairetu) {
		&syouhin_sprit($_);
		$syo_nedan *= 3;
		if($syo_kokugo<=0){$syo_kokugo="";}
		if($syo_suugaku<=0){$syo_suugaku="";}
		if($syo_rika<=0){$syo_rika="";}
		if($syo_syakai<=0){$syo_syakai="";}
		if($syo_eigo<=0){$syo_eigo="";}
		if($syo_ongaku<=0){$syo_ongaku="";}
		if($syo_bijutu<=0){$syo_bijutu="";}
		if($syo_kouka<=0){$syo_kouka="";}
		if($syo_looks<=0){$syo_looks="";}
		if($syo_tairyoku<=0){$syo_tairyoku="";}
		if($syo_kenkou<=0){$syo_kenkou="";}
		if($syo_speed<=0){$syo_speed="";}
		if($syo_power<=0){$syo_power="";}
		if($syo_wanryoku<=0){$syo_wanryoku="";}
		if($syo_kyakuryoku<=0){$syo_kyakuryoku="";}
		if($syo_love<=0){$syo_love="";}
		if($syo_unique<=0){$syo_unique="";}
		if($syo_etti<=0){$syo_etti="";}
		if($syo_zaiko <= 0){
			$kounyuubotan ="";
			$syo_zaiko = "売り切れ";
		}else{
			$kounyuubotan ="<input type=radio value=\"$syo_hinmoku,&,$syo_taikyuu,&,$syo_nedan,&,$syo_syubetu,&,\" name=\"syo_hinmoku\">"; #koko2006/08/22
		}
		if($syo_cal > 0){$calory_hyouzi = "$syo_cal kcal";}else{$calory_hyouzi = "ー";}
		if ($maeno_syo_syubetu ne "$syo_syubetu"){

			if($subetu){
				print <<"EOM";
				<tr>
				<td colspan=26><div align=center>
				個数 <select name="kosuu">
				$kazu_sentaku
				</select>支払い方法
				<select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
				<input type=submit value=" O K "></div>
				</td>
				</form>
				</tr>
				<form method="POST" action="$script">
				$depato_sele
EOM
			}
			$subetu++;
		
		print <<"EOM";
		<tr bgcolor=#ff9933><td align=center nowrap><a name=\"\#s_$subetu\"></a>▼$syo_syubetu</td><td align=center nowrap>在庫</td><td align=center>価格</td><td>国</td><td>数</td><td>理</td><td>社</td><td>英</td><td>音</td><td>美</td><td>ル</td><td>体</td><td>健</td><td>ス</td><td>パ</td><td>腕</td><td>脚</td><td>L</td><td>面</td><td>Ｈ</td><td align=center nowrap>カロリー</td><td align=center nowrap>耐久</td><td align=center>使用<br>間隔</td><td align=center>身体<br>消費</td><td align=center>頭脳<br>消費</td></tr>
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
#koko2007/10/09
		$mottru = 0;#koko2007/10/26
		foreach $tempo(@my_kounyuu_list){
			(@temporari) = split(/<>/,$tempo);
			if($syo_syubetu eq $temporari[0] && $syo_hinmoku eq $temporari[1]){
				if ($temporari[22] eq "日"){
					$keikanissuu = int ((time - $temporari[30]) / (60*60*24));
					$mottru = $temporari[21] - $keikanissuu;
				}else{
					$nokori = int($temporari[21] / $syo_taikyuu);
					if($temporari[21]%$syo_taikyuu){$mottru = $nokori+1;}else{$mottru = $nokori;}
				}
				last;
			}
		}
#koko2007/11/04
		if($kyokasuru == 2 || $kyokasuru == 1){
			$fukyoka = 0;
			foreach $temp0 (@kyokahitsuyou){
				if($syo_hinmoku eq $temp0){
					$fukyoka = 1;
				}
			}
		}

		if($fukyoka == 1 && $mottru && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"#ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $mottru){
			$in_hinmoku = "<font color=\"#ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"#ff0000\">$syo_hinmoku</font>";
		}elsif($fukyoka == 1){
			$in_hinmoku = "<font color=\"#ff0000\">$syo_hinmoku</font>"; #end2007/11/04
		}elsif($mottru){
			$in_hinmoku = "$kounyuubotan <font color=\"#0000ff\">$syo_hinmoku($mottru)</font>";
		}else{
			$in_hinmoku = "$kounyuubotan $syo_hinmoku";
		}
		
		print <<"EOM";
<tr bgcolor=#ffcc66 align=center><td width=150 align=left $disp_seru><label>$in_hinmoku</label></td><td align=right>$syo_zaiko</td><td align=right nowrap>$syo_nedan円</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
#kokoend
		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
#ver.1.30ここから
	print <<"EOM";
	<tr>
	<td colspan=26><div align=center>
	個数 <select name="kosuu">
	$kazu_sentaku
	</select>支払い方法
	<select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
	<input type=submit value=" O K "></div>
	</td>
	</form>
	</tr></table>
EOM
#ver1.30ここまで
	&hooter("login_view","戻る");
	exit;
}

####自動販売機　#koko2006/11/28
sub hanbai{
	open(IN,"< $hanbai_logfile") || &error("Open Error : $hanbai_logfile");
	eval{ flock (IN, 1); };
	$hanbai_kanri = <IN>;
	@syokudou_hairetu = <IN>;
	close(IN);
#koko2007/10/26 場所移動
	if(!$k_id){&error("mono.cgi エラー command2")} #koko2007/11/18
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
#koko2007/11/04
		if($kyokahin1 && $syo_hinmoku eq $kyokahin1 || $kyokahin2 && $syo_hinmoku eq $kyokahin2){ #koko2007/10/09
			$kyokasuru = 1;
		}elsif($kyokasuru != 1 && ($kyokahin1 || $kyokahin2)){
			$kyokasuru = 2;
		}
#end2007/11/04
	}
#end2007/10/26
	($hanbai_furag)=split(/<>/, $hanbai_kanri);
	my($sec,$min,$hour,$mday,$mon,$year) = localtime (time);
	if(($habaikoushin <= $hour && $hanbai_furag == 0) || $in{'sudoukoushin'} eq "yes"){##
		open(OL,"< $hanbai_detafile") || &error("Open Error : $hanbai_detafile");
		eval{ flock (OL, 1); };
		$hanbai_icigyo = <OL>;
		@new_syouhin_hairetu = ();
		while (<OL>){
			my $r = rand @new_syouhin_hairetu+1;
			push (@new_syouhin_hairetu,$new_syouhin_hairetu[$r]);
			$new_syouhin_hairetu[$r] = $_;
		}
		close(OL);
		$i=0;
		foreach (@new_syouhin_hairetu){
			&syouhin_sprit($_);
			if ($syo_syubetu eq "食"){next;}
#koko2006/11/21
			if ($hidensyouhin eq 'yes' && $syo_comment =~ /秘伝商品/){next;}
#kokoend
		#	$syo_zaiko = int($syo_zaiko/$zaiko_tyousetuti);
		#	if($syo_zaiko <= 0) {$syo_zaiko = 1;}
			&syouhin_temp;
			push (@new_syouhin_hairetu2,$syo_temp);
			$i ++;
			if ($i >= $habaisurukazu){last;}
		}
		@alldata = @new_syouhin_hairetu2;
		@keys0 = map {(split /<>/)[0]} @alldata;
		@alldata = @alldata[sort {@keys0[$a] cmp @keys0[$b]} 0 .. $#keys0];
		open(OLOUT,">$hanbai_logfile") || &error("$hanbai_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT "1<>$hour<>\n";
		print OLOUT @alldata;
		close(OLOUT);
		@syokudou_hairetu = @alldata;
	}elsif ($habaikoushin > $hour && $hanbai_furag == 1){###
		open(OLOUT,">$hanbai_logfile") || &error("$hanbai_logfileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT "0<>$hour<>\n";
		print OLOUT @syokudou_hairetu;
		close(OLOUT);
	}

	&header(syokudou_style);
	print <<"EOM";
	<form method="POST" action="$script">
	<input type=hidden name=mode value="buy_syouhin_hanbai">
	<input type=hidden name=name value="$in{'name'}">
	<input type=hidden name=pass value="$in{'pass'}">
	<input type=hidden name=k_id value="$in{'k_id'}">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<table width="100%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>自動販売機です。品揃えは毎日変わります。一度に持てる所有物の限度は$syoyuu_gendosuu品目です。<div class="honbun2">●$nameさんの所持金：$money円</div></td>
	<td bgcolor=#333333 align=center>自動販売機</td>
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
#koko2007/10/26
		$mottru = 0;
		foreach $tempo(@my_kounyuu_list){
			(@temporari) = split(/<>/,$tempo);
			if($syo_syubetu eq $temporari[0] && $syo_hinmoku eq $temporari[1]){
				if ($temporari[22] eq "日"){
					$keikanissuu = int ((time - $temporari[30]) / (60*60*24));
					$mottru = $temporari[21] - $keikanissuu;
				}else{
					$nokori = int($temporari[21] / $syo_taikyuu);
					if($temporari[21]%$syo_taikyuu){$mottru = $nokori+1;}else{$mottru = $nokori;}
				}
				last;
			}
		}
#koko2007/11/04
		if($kyokasuru == 2 || $kyokasuru == 1){
			$fukyoka = 0;
			foreach $temp0 (@kyokahitsuyou){
				if($syo_hinmoku eq $temp0){
					$fukyoka = 1;
				}
			}
		}

		if($fukyoka == 1 && $mottru && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $mottru){
			$in_hinmoku = "<font color=\"ff00ff\">$syo_hinmoku($mottru)</font>";
		}elsif($fukyoka == 1 && $kyokasuru == 1){
			$in_hinmoku = "$kounyuubotan <font color=\"ff0000\">$syo_hinmoku</font>";
		}elsif($fukyoka == 1){
			$in_hinmoku = "<font color=\"ff0000\">$syo_hinmoku</font>";
		}elsif($mottru){
			$in_hinmoku = "$kounyuubotan <font color=\"0000ff\">$syo_hinmoku($mottru)</font>";
		}else{
			$in_hinmoku = "$kounyuubotan $syo_hinmoku";
		}

		print <<"EOM";
<tr bgcolor=#ffcc66 align=center><td width=150 align=left $disp_seru><label>$in_hinmoku</label></td><td align=right>$syo_zaiko</td><td align=right nowrap>$syo_nedan円</td><td>$syo_kokugo</td><td>$syo_suugaku</td><td>$syo_rika</td><td>$syo_syakai</td><td>$syo_eigo</td><td>$syo_ongaku</td><td>$syo_bijutu</td><td>$syo_looks</td><td>$syo_tairyoku</td><td>$syo_kenkou</td><td>$syo_speed</td><td>$syo_power</td><td>$syo_wanryoku</td><td>$syo_kyakuryoku</td><td>$syo_love</td><td>$syo_unique</td><td>$syo_etti</td><td align=right nowrap>$calory_hyouzi</td><td nowrap>$taikyuu_hyouzi_seikei</td><td nowrap>$syo_kankaku分</td><td>$syo_sintai_syouhi</td><td>$syo_zunou_syouhi</td></tr>$disp_com
EOM
#kokoend end2007/10/26
		$maeno_syo_syubetu = "$syo_syubetu";
	}		#foreach閉じ
#ver.1.30ここから
#所有物チェック
	if(!$k_id){&error("mono.cgi エラー command3")} #koko2007/11/18
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
	print <<"EOM";
	<tr><td colspan=26><div align=center>
	支払い方法 <select name="siharaihouhou"><option value="現金">現金</option>$siharai_houhou</select>
	個数 <select name="kosuu">
EOM
for ($i=1 ; $i<=$item_kosuuseigen ; $i++){ 
			print "<option value=\"$i\">$i個</option> \n";
}
	print <<"EOM";
</select>
	　<input type=submit value=" O K "></div></td></tr>
	</table></form>
EOM
#ver1.30ここまで
	if ($in{'name'} eq $admin_name){
		print <<"EOM";
	<form method="POST" action="$script">
	<input type=hidden name=mode value="hanbai">
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

####購入処理販売機 #koko2006/11/28
sub buy_syouhin_hanbai {
	$kiroku = "hanbai";#koko2007/03/20
	$departset = 3;
	&buy_syouhin;
}

####購入処理 デパート２用 #koko2006/11/20
sub buy_syouhin2 {
	$kiroku = "depart_gamen2";#koko2007/03/20
	$departset = 2;
	&buy_syouhin;
}

####購入処理
sub buy_syouhin {
	if(!$kiroku){$kiroku = "depart_gamen";}

	if ($kaenai_seigen == 1){
		if ($k_id eq "$in{'ori_ie_id'}" || $house_type eq "$in{'ori_ie_id'}" && $in{'ori_ie_id'} ne ""){
			if($house_type){
				if (-e "./member/$house_type/log.cgi"){
					open(IN,"< ./member/$house_type/log.cgi") || &error("配偶者検索を行えません。");
					eval{ flock (IN, 1); };
					$oaitekensaku = <IN>;
					close(IN);
					&aite_sprit($oaitekensaku);
					if ($aite_house_type ne $k_id){
						$house_type = "";
					}else{
						&error("自分や配偶者のお店では商品を買うことができません。");
					}
				}else{
					$house_type = "";
				}
			}
		}
		if ($k_id eq "$in{'ori_ie_id'}"){&error("自分や配偶者のお店では商品を買うことができません。");}
	}

	($katta_syouhin,$katta_taikyuu,$katta_nedan,$katta_syubetu) = split(/,&,/,$in{'syo_hinmoku'});
	$katta_nedan*=$in{'kosuu'};
	$katta_taikyuu*=$in{'kosuu'};
	$katta_syubetu_b = $katta_syubetu;
	if ($in{'siharaihouhou'} eq "現金"){
		if ($katta_nedan > $money){&error("お金が足りません");}
	}

#自分の購入物ファイルにその商品があるかチェック
	if(!$k_id){&error("mono.cgi エラー command4")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 1); };
	@my_item_list = <OUT>;
	close(OUT);

	$gift_item_suu = 0;
	$my_item_suu = 0;

	foreach (@my_item_list){
		&syouhin_sprit($_);
#所属変更　ギフト・食料品
		if ($syo_kouka =~ m/ギフト/){$syo_syubetu = "ギフト";}
		if ($syo_taikyuu <= 0 && $syo_siyou_date + ($syo_kankaku*60) < $now_time){next;}
		if ($syo_syubetu eq "ギフト"){
			$gift_item_suu += 1;
			next;
		}
		if ($syo_syubetu eq "ギフト商品"){next;}
		if (!($syo_taikyuu <= 0)){
			$my_item_suu += 1;
		}
	}
#自分の住んでいる街かチェック
	&my_town_check($name);
	if ($return_my_town eq "$in{'town_no'}" && $k_id ne "$in{'ori_ie_id'}" && $in{'yakub'} ne "in"){
		$cashback_flag = "on";
		$cashback_kingaku = int ($katta_nedan / 10);
	}else{
		$cashback_flag = "off";
		if ($return_my_town ne "no_town" && $no_mytown eq 'yes' && $in{'ori_ie_id'} eq ""){
				&error("自分の街以外の購入はできません。");
		}
	}
	
	$katta_syouhin_tmp = $katta_syouhin;

	foreach $myneme(@urename){
		if ($katta_syouhin eq $myneme){$katta_syouhin = "$in{'name'}の$myneme";last;}
	}
	if ($katta_syouhin eq '子猫'){$katta_syouhin = "$in{'name'}の子猫";}

	$motteru_flag =0;
	@new_myitem_list = ();
	foreach (@my_item_list){
		&syouhin_sprit($_);

		$katta_syubetu = $katta_syubetu_b;
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
		
		if ($katta_syouhin eq $syo_hinmoku){
			$item_chc = 1;
		}

		if ($katta_syouhin eq $syo_hinmoku && $syo_syubetu ne "ギフト商品" && $syo_syubetu ne "ギフト" && $katta_syubetu eq $syo_syubetu){
			if ($syo_taikyuu_tani eq "回" || $syo_taikyuu_tani eq "日"){
				if ($syo_taikyuu_tani eq "日"){
					$syohin_no_taikyuu = int($katta_taikyuu / $in{'kosuu'});
					$keikanissuu = int ((time - $syo_kounyuubi) / (60*60*24));
					$nokoriset = int(($syo_taikyuu - $keikanissuu) / $syohin_no_taikyuu);
					$nokori = ($syo_taikyuu - $keikanissuu) % $katta_taikyuu;
					$kurikoshi = $nokoriset;
					if ($nokori){$nokoriset++;}
					if ($item_kosuuseigen <= $nokoriset){&error("これ以上このアイテムを増やすことはできません。");}
					$syo_kounyuubi = time;
					$syo_taikyuu = ($kurikoshi + $in{'kosuu'}) * $syohin_no_taikyuu + $nokori;
					$nokorinissuu = int($syo_taikyuu / $syohin_no_taikyuu);
					$motikosuu = $nokorinissuu;
				}else{
					$nokotteru_taikyuu = $syo_taikyuu;
					$syo_taikyuu += $katta_taikyuu;
					$syohin_no_taikyuu = int($katta_taikyuu / $in{'kosuu'});
					$motikosuu = int($syo_taikyuu / $syohin_no_taikyuu);
					if ($syo_taikyuu % $syohin_no_taikyuu > 0){$motikosuu++;}
					if ($item_kosuuseigen < $motikosuu){&error("このアイテムを$in{'kosuu'}個も増やすことはできません。");}
				}

				if($syo_taikyuu > 0){
					$tanka = 0;
					if ($cashback_flag eq "on"){
						$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan - $cashback_kingaku) / $syo_taikyuu);
					}else{
						$tanka = int (($tanka*$nokotteru_taikyuu + $katta_nedan) / $syo_taikyuu);
					}
				}
			}

			$motteru_flag =1;

			if ($in{'siharaihouhou'} ne "現金"){
				if($bank - $katta_nedan < 0){&error("貯金がありません。");}
				$bank -= $katta_nedan;
				&kityou_syori("クレジット支払い（$katta_syouhin）","$katta_nedan","",$bank,"普");
			}else{
				$money -= $katta_nedan;
			}
		}
		
		&syouhin_temp;
		push (@new_myitem_list,$syo_temp);
	}
	
	$katta_syouhin = $katta_syouhin_tmp;

	if (($gift_item_suu >= $kounyu_gift_gendo && $katta_syubetu eq "ギフト") || ($katta_syubetu ne "ギフト" && !$item_chc && $my_item_suu >= $syoyuu_gendosuu)){
		&error("これ以上所有できません。持ち物の所有限度数は$my_item_suu/$syoyuu_gendosuu ギフトの購入限度数$gift_item_suu/$kounyu_gift_gendoに達しています。");
	}

#持っていなかった場合
	if ($motteru_flag == 0){
#個人の店なら個人の店ログから商品パラメータをコピー
		if ($in{'ori_ie_id'}){
			$omise_log_file="./member/$in{'ori_ie_id'}/omise_log.cgi";
			open(KOM,"< $omise_log_file") || &error("Open Error : $omise_log_file");
			eval{ flock (KOM, 1); };
			@kounyuu_hairetu = <KOM>;
			close(KOM);
#デパートならデパートログより商品パラメータをコピー
		}elsif ($departset == 2){
			open(KOM,"< $depart_logfile2") || &error("Open Error : $depart_logfile2");
			eval{ flock (KOM, 1); };
			@kounyuu_hairetu = <KOM>;
			close(KOM);
		}elsif($departset == 3){
			open(KOM,"< $hanbai_logfile") || &error("Open Error : $hanbai_logfile");
			eval{ flock (KOM, 1); };
			$hanbai_kanri = <KOM>;
			@kounyuu_hairetu = <KOM>;
			close(KOM);
		}else{
			open(KOM,"< $depart_logfile") || &error("Open Error : $depart_logfile");
			eval{ flock (KOM, 1); };
			@kounyuu_hairetu = <KOM>;
			close(KOM);
		}

		$kounyuu_ok = 0;
		foreach (@kounyuu_hairetu){
			&syouhin_sprit($_);
			if ($syo_kouka =~ m/ギフト/){
				$syo_syubetu = "ギフト";
			}
			if ($syo_kouka =~ m/食料品/){
				$syo_syubetu = "食料品";
			}
			if ($syo_kouka =~ m/ファ/){
				$syo_syubetu = "ファーストフード";
			}

			if ($katta_syouhin eq "$syo_hinmoku"){
				$syo_taikyuu*=$in{'kosuu'};
				$oboe_syubetu = $syo_syubetu;
				$syo_kounyuubi = time;
				if ($cashback_flag eq "on"){
					$tanka = int (($katta_nedan - $cashback_kingaku) / $syo_taikyuu);
				}else{
					$tanka = int ($katta_nedan / $syo_taikyuu);
				}

				foreach $myneme(@urename){
					if ($syo_hinmoku eq $myneme){
						$syo_hinmoku = "$in{'name'}の$myneme";
						last;
					}
				}
				if ($syo_hinmoku eq '子猫'){$syo_hinmoku = "$in{'name'}の子猫";}

				&syouhin_temp;
				push (@new_myitem_list,$syo_temp);
				if ($in{'siharaihouhou'} ne "現金"){
				if($bank - $katta_nedan < 0){&error("貯金がありません。");}
					$bank -= $katta_nedan;
					&kityou_syori("クレジット支払い（$katta_syouhin）","$katta_nedan","",$bank,"普");
				}else{
					$money -= $katta_nedan;
				}
				
				$kounyuu_ok = 1;
				last;
			}
		}
		if ($kounyuu_ok == 0){&error("$katta_syouhin購入できませんでした。");}
	}
	&lock;

#個人のお店なら在庫を引いてお金を入金＆記帳
	if ($in{'ori_ie_id'}){
		$omise_log_file="./member/$in{'ori_ie_id'}/omise_log.cgi";
		open(SYO,"< $omise_log_file") || &error("Open Error : $omise_log_file");
		eval{ flock (SYO, 1); };
		@omise_zan = <SYO>;
		close(SYO);
		@new_omise_zan=();
		$syo_atta_fg=0;
		foreach (@omise_zan){
			&syouhin_sprit($_);
			if($katta_syouhin eq "$syo_hinmoku"){
				if ($syo_zaiko <= 0){&error("在庫切れです");}
				$syo_zaiko = $syo_zaiko-$in{'kosuu'} ;
				$syo_atta_fg=1;
			}
			if ($syo_zaiko <= 0){next;}
			&syouhin_temp;
			push (@new_omise_zan,$syo_temp);
		}
		if($syo_atta_fg==0){&error("在庫がありません。3");};

		open(OLOUT,">$omise_log_file") || &error("$omise_log_fileに書き込みが出来ません");
		eval{ flock (OLOUT, 2); };
		print OLOUT @new_omise_zan;
		close(OLOUT);
#相手の銀行に振り込み＆記帳処理
		if ($k_id ne "$in{'ori_ie_id'}"){#自分の店なら売上金は入らない
			&openAitelog ($in{'ori_ie_id'});
			$aite_bank += $katta_nedan;
			&aite_kityou_syori("販売（$katta_syouhin） => $in{'name'}さん","",$katta_nedan,$aite_bank,"普",$in{'ori_ie_id'},"lock_off");

			&aite_temp_routin;
			open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
			eval{ flock (OUT, 2); };
			print OUT $aite_k_temp;
			close(OUT);
		}

#自分の住んでいる街のお店ならキャッシュバック
		if ($cashback_flag eq "on" and $k_id ne "$in{'ori_ie_id'}"){
			$money += $cashback_kingaku;
			$cashback_message = "<br>★ご近所店特典として、$cashback_kingaku円がキャッシュバックされました。";
		}

#街の経済力アップ
		&town_keizaiup($katta_nedan,$in{'town_no'});
	}else{
#デパートなら在庫を引く
		if ($departset == 2){
			open(SYO,"< $depart_logfile2") || &error("Open Error : $depart_logfile2");
			eval{ flock (SYO, 1); };
			@depa_zan = <SYO>;
			close(SYO);
		}elsif ($departset == 3){
			open(SYO,"< $hanbai_logfile") || &error("Open Error : $hanbai_logfile");
			eval{ flock (SYO, 1); };
			$hanbai_kanri = <SYO>;
			@depa_zan = <SYO>;
			close(SYO);
		}else{
			open(SYO,"< $depart_logfile") || &error("Open Error : $depart_logfile");
			eval{ flock (SYO, 1); };
			@depa_zan = <SYO>;
			close(SYO);
		}

		@new_depa_zan=();
		$syo_atta_fg=0;
		foreach (@depa_zan){
			&syouhin_sprit($_);
			if($katta_syouhin eq "$syo_hinmoku"){
			$syo_nokori=$syo_zaiko-$in{'kosuu'};
				if ($syo_nokori < 0){&error("在庫切れ、または在庫がそんなにありません。");}
				$syo_zaiko = $syo_nokori ;
				$syo_atta_fg=1;
			}
			if ($syo_zaiko <= 0){next;}
			&syouhin_temp;
			push (@new_depa_zan,$syo_temp);
		}
		if($syo_atta_fg==0){&error("在庫がありません。4");}

		if ($departset == 2){
			open(OLOUT,">$depart_logfile2") || &error("$depart_logfile2に書き込みが出来ません");
			eval{ flock (OLOUT, 2); };
			print OLOUT @new_depa_zan;
			close(OLOUT);
		}elsif($departset == 3){
			open(OLOUT,">$hanbai_logfile") || &error("Open Error : $hanbai_logfile");
			eval{ flock (OLOUT, 2); };
			print OLOUT $hanbai_kanri;
			print OLOUT @new_depa_zan;;
			close(OLOUT);
		}else{
			open(OLOUT,">$depart_logfile") || &error("$depart_logfileに書き込みが出来ません");
			eval{ flock (OLOUT, 2); };
			print OLOUT @new_depa_zan;
			close(OLOUT);
		}
	}	#デパート購入の場合の閉じ

#自分の購入物ファイルのログ更新
	if(!$k_id){&error("mono.cgi エラー command5")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,">$monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_list;
	close(OUT);

	if (-z $monokiroku_file){
		$loop_count = 0;
		while ($loop_count <= 10){
			for (0..50){$i=0;}
			@f_stat_b = stat($monokiroku_file);
			$size_f = $f_stat_b[7];
			if ($size_f == 0 && @new_myitem_list ne ""){
				open (OUT, "> $monokiroku_file") or &error("エラー・ファイルが開けません $monokiroku_file");
				eval{ flock (OUT, 2); };
				print OUT @new_myitem_list;
				close (OUT);
			}else{
				last;
			}
			$loop_count++;
		}
	}

	&unlock;
	
#ログ更新
	&temp_routin;
	&log_kousin($my_log_file,$k_temp);

	&header("","sonomati");

	if (!$motikosuu && $oboe_syubetu eq "ギフト"){
		$gift_item_suu++;
		$motikosuu = 0;
	}elsif(!$motikosuu){
		$motikosuu = 1;
		$my_item_suu++;
	}

#クーポンゲットここから
	$coupon_rand = int(rand(7))+1;
	if($coupon_rand == 1){
		$coupon_rand2 = int(rand(5))+1;
		&coupon_get($coupon_rand2);
		$coupon_message = "<br>★クーポン券を$coupon_rand2枚もらいました";
	}

	print <<"EOM";
	<div align=center><br><table border=0 cellspacing="5" cellpadding="0" width=300 style="$message_win"><tr><td>
	<span class="job_messe">
	●$katta_syouhinを$in{'kosuu'}個購入しました。
	<br>ギフトは$gift_item_suu個です。$cashback_message$coupon_message
	<br>現在のアイテム所持数は$my_item_suu個です。$motikosuuセットあります。
	</span><br>
	<br>
持ち金：<span id="money_down">$money</span>円
<script type="text/javascript"><!-- 
money_down();
function money_down(){
	var syo_value = $katta_nedan;
	var last_value = $money;
	var money_value = last_value + syo_value;
	var TH;
	TH = setInterval(function() {
		money_value -= Math.floor(syo_value/30);
		if (money_value <= last_value) {
			document.getElementById("money_down").innerText = last_value;
			clearInterval(TH);
		}else{
			document.getElementById("money_down").innerText = money_value;
		}
	}, 50);
}
 --></script>

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

#メッセージ送信
sub mail_sousin {
	if($in{'name'} eq "Eliwood"){
		&error("メンテナンス中・・・");
	}
	
	$genzai_zikoku = time;
	open(GUEST,"< $guestfile") or &error("エラー・ファイルが開けません $guestfile");
	eval{ flock (GUEST, 1); };
	@all_guest=<GUEST>;
	close(GUEST);
	@new_all_guest = ();
	foreach (@all_guest) {
		($sanka_timer,$sanka_name,$hyouzi_check) = split(/<>/);
		if ($name eq "$sanka_name"){
			$sanka_timer = $genzai_zikoku;
		}
		$sanka_tmp = "$sanka_timer<>$sanka_name<>$hyouzi_check<>$in{'town_no'}<>\n";
		push (@new_all_guest,$sanka_tmp);
	}
    
	if ($mem_lock_num == 0){
		$err = &data_save($guestfile, @new_all_guest);
		if ($err) {&error("$err");}
	}else{
		&lock;	
		open(GUEST,">$guestfile") or &error("エラー・ファイルが開けません $guestfile");
		eval{ flock (GUEST, 2); };
		print GUEST @new_all_guest;
		close(GUEST);
		&unlock;
	}
    
	#自分のメールログを開いてアクセス時間を書き込み＆ログを読み込み
	$message_file="./member/$k_id/mail.cgi";
	open(TIMEIN,"< $message_file") || &error("Open Error : $message_file");
	eval{ flock (TIMEIN, 1); };
	$now_time= time;
	$last_m_check = <TIMEIN>;
	#表示用の配列
	@my_mail_data = <TIMEIN>;
	$soumailkensuu = @my_mail_data;
	$last_m_check = "$now_time\n";
	close(TIMEIN);
    
	if ($in{'del'} ne ""){
		$loop_i2 = 0;
		$loop_max = @my_mail_data;
		for($loop_i=0;$loop_i<$loop_max;$loop_i++){
			if ($in{"del".$loop_i} eq ""){
				$loop_i2++;
				next;
			}
			&mail_sprit($my_mail_data[$loop_i2]);
			if ($in{"del".$loop_i} ne $m_date){&error("削除エラー");}
			splice @my_mail_data,$loop_i2,1;
		}
		open(TIMEIN,"> $message_file") || &error("Open Error : $message_file");
		eval{ flock (TIMEIN, 2); };
		print TIMEIN $last_m_check;
		print TIMEIN @my_mail_data;
		close(TIMEIN);
		
		$soumailkensuu = @my_mail_data;
	}
	
	$friend_file="./member/$k_id/friend.cgi";
	if (-e $friend_file){
		open(IN,"<$friend_file") || &error("$friend_fileが開けません");
		eval{ flock (IN, 2); };
		@friend_data = <IN>;
		foreach(@friend_data){
			chomp $_;
			$friend_list .= "<option value=\"$_\">$_</option>\n";
		}
		close(IN);
	}
	
	#持ち物リストからギフト配列作成
	if(!$k_id){&error("mono.cgi エラー command6")}
	$monokiroku_file="./member/$k_id/mono.cgi";
	open(OUT,"< $monokiroku_file") || &error("Open Error : $monokiroku_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "ギフト"){
			$gift_select .= "<option value=\"$syo_hinmoku\">$syo_hinmoku</option>\n";
		}
	}

	# 最終アクセス時間を更新
	&lock;
	#書き込み用の配列を初期化
	@my_kakikomi_mail_data = ();
	push (@my_kakikomi_mail_data,@my_mail_data);
	unshift (@my_kakikomi_mail_data,$last_m_check);
	if ($soumailkensuu > $mail_hozon_gandosuu){pop @my_kakikomi_mail_data;}		#ver.1.3
	open(TIMEOUT,">$message_file") || &error("Write Error : $message_file");
	eval{ flock (TIMEOUT, 2); };
	print TIMEOUT @my_kakikomi_mail_data;
	close(TIMEOUT);
	
	&unlock;
	&header(item_style);
	
	print <<"EOM";
	<table width="95%" border="0" cellspacing="0" cellpadding="10" align=center class=yosumi>
	<tr>
	<td bgcolor=#ffffff>相手の方の名前を入力してメッセージを送信することができます。受信箱と送信箱にメッセージが残っている相手はアドレス帳に追加されます。このアドレス帳から名前を選べば名前欄の入力は必要ありません。<br>
	※保存しておけるメッセージは「受信箱」「送信箱」合わせて$mail_hozon_gandosuu件で、これを超えると古いメッセージから削除されます。<br>
	※「ギフト」カテゴリーの商品を持っていれば、プレゼント送付でその商品を選び、メールと同時に送付することができます。</td>
	<td bgcolor="#ffcc00" align=center width="300"><font color="#333333" size="5"><b>メ　ー　ル</b></font></td>
	</tr></table><br>
EOM
	@address_match = ();
	LOOP : foreach $mail_data_add (@my_mail_data){
		&mail_sprit($mail_data_add);
		foreach $maenideta_ad (@address_match){
			if ($maenideta_ad eq $m_name) {next LOOP;}
		}
		if($m_name =~ /不定期新聞ＫＩＮＫＩ/){next LOOP;}
		if($m_name =~ /副管理人（/){next LOOP;}
		
		$addresstyou .= "<option value=\"$m_name\">$m_name</option>\n";
		push (@address_match ,$m_name);
	}
	
	&hooter("login_view","街に戻る",'','yes');
	print <<"EOM";
<SCRIPT type="text/javascript" language="JavaScript">
<!--
function Navi_m(mode, aite, kod_num, event) {
	if(document.getElementById("set_" + mode).style.display == ""){document.getElementById("set_" + mode).style.display = "none";}
	else{document.getElementById("set_" + mode).style.display = "";}
	if(!event) var event=window.event;
	if(!event.pageX) event.pageX = event.clientX + document.body.scrollLeft;
	if(!event.pageY) event.pageY = event.clientY + document.body.scrollTop;
	
	document.getElementById("set_" + mode).style.left = event.pageX - 315;
	document.getElementById("set_" + mode).style.top = event.pageY + 15;
	
	if(kod_num){
		document.getElementById("kod_num").value = kod_num;
	}
	document.getElementById("name_" + mode).value = aite;
	return false;
}
//-->
</SCRIPT>

<table style="position:absolute;display:none;z-index:5;background-color:#eeeeee;" border="1" cellpadding="5" cellspacing="0" id="set_propose">
	<form method="POST" action="kekkon.cgi">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>kokuhaku<>">
	<input type=hidden name=command value="propose_ok">
	<input type=hidden name="sousinsaki_name" id="name_propose">
	<tr><td>
	
	メッセージ <input type=text name=m_com size=30>
	<input type=submit value="結婚をOKする">
	<div class=small>
		※結婚OKの場合、メッセージを入れて「結婚をOKする」ボタンを押してください。<br>
		　断る場合、何もする必要はありません。
	</div>
	
	</td></tr>
	</form>
</table>

<table style="position:absolute;display:none;z-index:5;background-color:#eeeeee;" border="1" cellpadding="5" cellspacing="0" id="set_kousai">
	<form method="POST" action="kekkon.cgi">
	<input type=hidden name=my_data value="$name<>$pass<>$k_id<>$in{'town_no'}<>kokuhaku<>">
	<input type=hidden name=command value="kousai_ok">
	<input type=hidden name="sousinsaki_name" id="name_kousai">
	<tr><td>
	
	メッセージ <input type=text name=m_com size=30><input type=submit value="交際をOKする">
	<div class=small>
		※交際OKの場合、メッセージを入れて「交際をOKする」ボタンを押してください。<br>
		　断る場合、何もする必要はありません。
	</div>
	
	</td></tr>
	</form>
</table>

<table style="position:absolute;display:none;z-index:5;background-color:#eeeeee;" border="1" cellpadding="5" cellspacing="0" id="set_kodomo">
	<form method="POST" action="kekkon.cgi">
	<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>kodomo_naming<>">
	<input type=hidden name="kod_num" id="kod_num">
	<input type=hidden name="sousinsaki_name" id="name_kodomo">
	<tr><td>
	
	子供のお名前（全角10文字以内） <input type=text name=kodomo_name size=20>
	<select name="umu_umanai">
	<option value="umu">この名前で出産する</option>
	<option value="umanai">産まない</option>
	</select>
	<input type=submit value=" O K ">	
	<div class=small>
		※子供の名前を決めてOKボタンを押してください。<br>
		　あとで変更はできませんので、お相手の方とよくご相談してから決めてください。<br>
		　出産しない場合は、「産まない」を選んでOKボタンを押してください。<br>
		　また$kodomo_sibou_time日間のうちにこの作業をしないと出産できなくなります。<br>
	</div>
	
	</td></tr>
	</form>
</table>


<table width="100%" border="0" cellspacing="10" cellpadding="0" align=center>
<tr><td width=50% valign=top>
	<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
	<form method="POST" action="$script">
	<input type=hidden name=mode value="mail_do">
	<input type=hidden name=name value="$name">
	<input type=hidden name=pass value="$pass">
	<input type=hidden name=id value="$k_id">
	<input type=hidden name=town_no value="$in{'town_no'}">
	<tr><td>
		<div class=tyuu>■メッセージ送信</div>
		●送信先の名前<br>
		<input type=text size=50 name="sousinsaki_name" value="$in{'sousinsaki_name'}">
		<select name="sousinsaki_name3">
		<option value="" style="font-weight: bold;">友達リスト</option>
		$friend_list
		</select>
		<select name="sousinsaki_name2">
		<option value="" style="font-weight: bold;"">アドレス帳</option>
		$addresstyou
		</select><br>
		●メッセージ<br>
		<textarea cols=58 rows=8 name=m_com wrap="soft"></textarea><br>
	</td></tr>
	<tr><td>
		●プレゼント送付<br>
		<select name=gift_souhu>
		<option value="">無し</option>
		$gift_select
		</select>
		<input type=text size=3 name="okurisuu" value="1">回（日）分を送る。
		<br>
		●Ｋポイント送付<br>
		<input type=text size=5 name="okuru_kpoint" value="0">Ｐ送る。<br><br>
	</td></tr>
	<tr><td align=center colspan="2">
		<input type="button" value="送信する" onclick="if( confirm('内容はこれでよいですか？') ){this.form.submit();}">
	</td></tr>
	</form>
	</table>
</td></tr>
</table>

<table width="100%" border="0" cellspacing="10" cellpadding="0" align=center>
<form method="POST" action="$script">
<input type="hidden" name="my_data" value="$name<>$pass<>$k_id<>$in{'town_no'}<>mail_sousin<>">
<input type="hidden" name="del" value="on">
<tr><td width="100%" align="center" colspan="2"><input type="submit" value="選択したメールを消去"></td></tr>
<tr><td width=50% valign=top>
	<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
	<tr><td>
	<div class=tyuu>■送信箱</div>
EOM
	$i=0;
	
	$loop_i =0;
	foreach (@my_mail_data){
		&mail_sprit ($_);
		
		if ($m_syubetu eq "送信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんへ送ったメッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif($m_syubetu eq "告白送信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんへ送った交際申\し込みメッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif($m_syubetu eq "プロポ送信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんへ送ったプロポーズメッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif($m_syubetu eq "プロポ承諾送信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんへ送った結婚承諾メッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif($m_syubetu eq "交際承諾送信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんへ送った交際承諾メッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}
		$loop_i++;
	}
	if ($i == 0){print "<br><br>まだ送信したメッセージ</label>はありません。";}
	print <<"EOM";
	</td></tr></table>
</td><td width=50% valign=top>
	<table border="0" cellspacing="0" cellpadding="10" class=yosumi width=100%>
	<tr><td>
	<div class=tyuu>■受信箱</div>
EOM
	$i=0;
	
	$loop_i =0;
	foreach (@my_mail_data){
		&mail_sprit ($_);
		
		if ($m_syubetu eq "受信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんからのメッセージ</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif ($m_syubetu eq "告白受信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんから交際のお申\し込みがありました</label>
</div>
$m_com<br>
<br>
<a href=kekkon.cgi?mode=assenjo&command=easySerch&serch_name=$m_name&town_no=$in{'town_no'}&name=$name&pass=$pass>恋人斡旋所で$m_nameさんのプロフィールを見る</a>
<br>
<div class=honbun2 onclick="Navi_m('kousai','$m_name','',event)"><input type="button" value="交際承諾フォーム出現"></div>
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif ($m_syubetu eq "プロポ受信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんからプロポーズされました。</label>
</div>
$m_com<br>
<br>
<a href=kekkon.cgi?mode=assenjo&command=easySerch&serch_name=$m_name&town_no=$in{'town_no'}&name=$name&pass=$pass>恋人斡旋所で$m_nameさんのプロフィールを見る</a>
<br>
<div class=honbun2 onclick="Navi_m('propose','$m_name','',event)"><input type="button" value="プロポース承諾フォーム出現"></div>
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif ($m_syubetu eq "プロポ承諾受信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">おめでとうございます。$m_nameさんから結婚OKのお返事が来ました。</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif ($m_syubetu eq "交際承諾受信"){
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">おめでとうございます。$m_nameさんから交際OKのお返事が来ました。</label>
</div>
$m_com
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}elsif ($m_syubetu eq "出産" || $m_syubetu eq "男出産" || $m_syubetu eq "女出産"){
		
			if($m_syubetu eq "男出産"){$disp_ko = "<font color=#3366cc>元気な男の子</font>";}
			elsif($m_syubetu eq "女出産"){$disp_ko = "<font color=#ff3366>可愛い女の子</font>";}
			else{$disp_ko = "子供";}
			
			print <<"EOM";
<hr size=1>
<div style="color:#ff3366">
	<input type="checkbox" name="del$loop_i" value="$m_date" id="del$loop_i">
	<label for="del$loop_i">$m_nameさんとの間に$disp_koができました。</label>
</div>
<br>
<div class=honbun2 onclick="Navi_m('kodomo','$m_name','$m_com',event)"><input type="button" value="子供出産フォーム出現"></div>
<div class=small align=right>（$m_date）</div>
EOM
			$i ++;
		}
		$loop_i++;
	}
	if ($i == 0){print "<br><br>まだ受信したメッセージはありません。";}
	print "</td></tr></table></form></td></tr></table>";

		&hooter("login_view","戻る");
	exit;
}

#メール送信処理
sub mail_do {
	if($in{'name'} ne $admin_name){
		if($in{'okuru_kpoint'} and $in{'okuru_kpoint'} =~ /[^0-9]/){&error("半角数字で記入してください");}
	}
	
	if($in{'okurisuu'} and $in{'okurisuu'} =~ /[^0-9]/){&error("半角数字で記入してください");}
	if ($in{'command'} ne 'from_system' && ($in{'sousinsaki_name'} eq $in{'name'} || $in{'sousinsaki_name2'} eq $in{'name'} || $in{'sousinsaki_name3'} eq $in{'name'})){&error("自分に送っても意味ありません。");}
	if ($in{'sousinsaki_name'} eq "" && $in{'sousinsaki_name2'} eq "" && $in{'sousinsaki_name3'} eq ""){&error("相手先のお名前の入力がありません");}
	if ($in{'m_com'} eq ""){&error("メッセージが入力されていません");}
	if ($in{'sousinsaki_name2'}){$aite_name = "$in{'sousinsaki_name2'}";}
	elsif ($in{'sousinsaki_name3'}){$aite_name = "$in{'sousinsaki_name3'}";}
	else{$aite_name = "$in{'sousinsaki_name'}";}
	if ($in{'m_com'} !~ /(\x82[\x9F-\xF2])|(\x83[\x40-\x96])/) { &error("日本語を書いてください。"); } 
        
	&id_check ($aite_name);
	if ($in{'gift_souhu'}){
		if ($aite_name eq $name){&error("自分に贈ることはできません");}
		if ($in{'cou_k_id'}){
			&cou_uketori;
		}else{
			&gift_souhu_syori;#中でロック
		}
	}
	
	if ($in{'okuru_kpoint'}){
		$kpoint -= $in{'okuru_kpoint'};
		if($kpoint<0){&error("そんなにＫポイント持ってませんよ。");}
		&temp_routin;
		&log_kousin($my_log_file,$k_temp);
		
		&openAitelog ($return_id);
		$aite_kpoint += $in{'okuru_kpoint'};
		&aite_temp_routin;
		
		open(OUT,">$aite_log_file") || &error("$aite_log_fileが開けません");
		eval{ flock (OUT, 2); };
		print OUT $aite_k_temp;
		close(OUT);
	}
		
	$message_file="./member/$return_id/mail.cgi";
	open(AIT,"< $message_file") || &error("お相手の方のメール記録ファイル（$message_file）が開けません。");
	eval{ flock (AIT, 1); };
	$last_mail_check_time = <AIT>;
	@mail_cont = <AIT>;
	close(AIT);
       
	$in{'m_com'} =~ s/<>/&lt;&gt;/g;
	$in{'m_com'} =~ s/\r\n/<br>/g;
	$in{'m_com'} =~ s/\r/<br>/g;
	$in{'m_com'} =~ s/\n/<br>/g;
	
	$m_comment = "$in{'m_com'}<div class=honbun2>";
	if ($in{'gift_souhu'}){
		$m_comment .= "<br>『$in{'gift_souhu'}』が$in{'okurisuu'}回（日）分贈られてきました。";
	}
	if ($in{'okuru_kpoint'}){
		$m_comment .= "<br>Ｋポイントが$in{'okuru_kpoint'}Ｐ贈られてきました。";
	}
	$m_comment .= "</div>";
	&time_get;
	if ($in{'command'} eq 'from_system'){$okuri = $admin_name}else{$okuri = $in{'name'};}
	$new_mail = "受信<>$okuri<>$m_comment<>$date2<>$date_sec<><><><><><>\n";
	unshift (@mail_cont,$new_mail);
	if (@mail_cont > $mail_hozon_gandosuu){pop @mail_cont;}
		
	#最終メールチェック時間がなければ１を入れる
	if ($last_mail_check_time eq ""){$last_mail_check_time = "1\n";}
	unshift (@mail_cont,$last_mail_check_time);
	&lock;
	open(OUT,">$message_file") || &error("$message_fileに書き込めません");
	eval{ flock (OUT, 2); };
	print OUT @mail_cont;
	close(OUT);
	&unlock;

	#自分のメールにも送信済みメッセージとして記録（管理者メールでなければ）
	if ($in{'command'} ne "from_system"){
		$my_sousin_file="./member/$k_id/mail.cgi";
		open(ZIB,"< $my_sousin_file") || &error("$my_sousin_fileが開けません。");
		eval{ flock (ZIB, 1); };
		$my_last_mail_check_time = <ZIB>;
		@my_mail_cont = <ZIB>;
		close(ZIB);
		$my_m_comment = "$in{'m_com'}<div class=honbun2>";
		if ($in{'gift_souhu'}){
			$my_m_comment .= "<br>『$in{'gift_souhu'}』を$in{'okurisuu'}回（日）分を贈りました。";
		}
		if ($in{'okuru_kpoint'}){
			$my_m_comment .= "<br>Ｋポイントを$in{'okuru_kpoint'}Ｐ贈りました。";
		}
		$my_m_comment .= "</div>";
		$sousin_mail = "送信<>$aite_name<>$my_m_comment<>$date2<>$date_sec<><><><><><>\n";
		unshift (@my_mail_cont,$sousin_mail);
		if (@my_mail_cont > $mail_hozon_gandosuu){pop @my_mail_cont;}
		
		#最終メールチェック時間がなければ今の時間を入れる
		if ($my_last_mail_check_time eq ""){$my_last_mail_check_time = "$date_sec\n";}
		unshift (@my_mail_cont,$my_last_mail_check_time);
		&lock;
		open(ZIBO,">$my_sousin_file") || &error("$my_sousin_fileに書き込めません");
		eval{ flock (ZIBO, 2); };
		print ZIBO @my_mail_cont;
		close(ZIBO);
		&unlock;
	}
    
	if ($in{'command'} ne "from_system"){
		&message_only("$aite_nameさんへメッセージを送信しました。");
		&hooter("mail_sousin","メール画面へ",'','yes');
		&hooter("login_view","戻る");
	}else{
		&message("$aite_nameさんへメッセージを送信しました。","itiran","admin.cgi");
	}
	exit;
}

#ギフト送付処理
sub gift_souhu_syori {
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
		if ($syo_hinmoku eq "$in{'gift_souhu'}" && $syo_syubetu eq "ギフト" && $monoatta_flag == 0){
			if ($syo_taikyuu < $in{'okurisuu'}){&error("そんなに耐久ありません。");}
			$syo_taikyuu -= $in{'okurisuu'}; #koko2007/08/04
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
	if($in{'okurisuu'} =~ /[^0-9]/){&error("個数は半角数字で記入してください");}
	if($in{'okurisuu'} =~ /-/){&error("回（日）数マイナスは禁止");}
	if($in{'okurisuu'} <= 0){&error("回（日）数が0以下になっています。");}
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
	$syo_taikyuu = $in{'okurisuu'};
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
			$syo_taikyuu+=$in{'okurisuu'};
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
########## 管理者個人配達
sub cou_uketori{
	$prezento_file="./dat_dir/prezento.cgi";
	open(OUT,"< $prezento_file") || &error("Open Error : $prezento_file");
	eval{ flock (OUT, 1); };
	@myitem_hairetu = <OUT>;
	close(OUT);
	$monoatta_flag = 0;
	@new_myitem_hairetu =();#koko2007/06/05
	foreach (@myitem_hairetu){
		&syouhin_sprit($_);
#koko2007/07/23 クーポン #koko2007/10/29
		if ($syo_hinmoku eq "$in{'gift_souhu'}" && $syo_syubetu ne "ギフト商品" && $syo_hinmoku ne "クーポン" && !$monoatta_flag){
			$ageru_gift_copy = "$_";
			$monoatta_flag = 1;
			last;
		} #koko2006/10/20
		if ($syo_hinmoku eq "クーポン" && $in{'gift_souhu'} eq "クーポン" && !$monoatta_flag){
			$ageru_gift_copy = "$_";
			$cou_syo_taikyuu = $syo_taikyuu;
			$monoatta_flag = 1;
			last;
		}
	}
	if ($monoatta_flag == 0){&error("既に商品はありません。");}

# 購入日を記録、単価は0円、種別をギフト商品にする
	&syouhin_sprit($ageru_gift_copy);
	$syo_kounyuubi = time;
	$tanka = 0;

#	if ($syo_hinmoku ne "クーポン"){
#		$syo_syubetu = "ギフト商品";
#	}

	#koko2006/10/09
	$syo_kouka =~ s/,ギフト//g;
	$syo_kouka =~ s/ギフト//g;
	($syo_comment) = split(/\t/,$syo_comment);
	$syo_comment .= "\t管理者からの贈り物です。";
	#kokoend
	if ($syo_hinmoku eq "クーポン"){
		$syo_syubetu = 'ギフト';
		$syo_taikyuu = $cou_syo_taikyuu;
		$coupon_okuri =1;
	}
	&syouhin_temp;
	$okuraretamono = $syo_temp;
#相手の持ち物リストに商品を追加
	if(!$in{'cou_k_id'}){&error("IDが存在しません。command9");} #koko2007/10/19
	$aite_monokiroku_file="./member/$in{'cou_k_id'}/mono.cgi";
	open(ASP,"< $aite_monokiroku_file") || &error("Open Error : $aite_monokiroku_file");
	eval{ flock (ASP, 1); };
	@aite_item_hairetu = <ASP>;
	close(ASP);
#koko2007/07/23 クーポン
	@new_aite_item_hairetu = ();
	$kupon_okuri = 0;
	$syubetu = $syo_syubetu;
	$hinmoku = $syo_hinmoku;
	$taikyuu = $syo_taikyuu;
	foreach (@aite_item_hairetu){
		&syouhin_sprit($_);
		if ($syo_syubetu eq "ギフト" && $syo_hinmoku eq $hinmoku && $coupon_okuri){
			$syo_taikyuu += $cou_syo_taikyuu;
			$motteru = 1;
		}elsif ($syo_syubetu eq $syubetu && $syo_hinmoku eq $hinmoku){
			$syo_taikyuu += $taikyuu;
			$motteru = 1;
		}
		&syouhin_temp;
		push @new_aite_item_hairetu,$syo_temp;
	}
	if ($motteru != 0){
		@aite_item_hairetu = (@new_aite_item_hairetu);

#	}elsif ($gift_count >= $gift_gendo){&error("お相手の方のギフトが限度数の$gift_gendoを超えるため送付できません");
	}else{
		push (@aite_item_hairetu,$okuraretamono);
	}
#相手の所有物ファイルを更新
	open(ASP,">$aite_monokiroku_file") || &error("Write Error : $aite_monokiroku_file");
	eval{ flock (ASP, 2); };
	print ASP @aite_item_hairetu;
	close(ASP);	

}

###### クーポン処理 ######
sub coupon_get{
	$coupointo = $_[0];
	$monokiroku_file="./member/$k_id/mono.cgi";
	if (! -e $monokiroku_file){open (OUT,">$monokiroku_file") || &error("自分の購入物ファイルを作成できません");}
	close(OUT);
	open(OUT,"< $monokiroku_file") || &error("自分の購入物ファイルが開けません");
	eval{ flock (OUT, 2); };
	@my_kounyuu_list =<OUT>;
	close(OUT);

	$kensa_flag=0;
	@new_myitem_hairetu = (); #koko2006/06/05
	foreach $one_kounyuu_item (@my_kounyuu_list){
		&syouhin_sprit ($one_kounyuu_item);
		if ($syo_syubetu eq 'ギフト' && $syo_hinmoku eq 'クーポン'){
			$syo_taikyuu += $coupointo;
			$kensa_flag = 1;
		}
		&syouhin_temp;
		push @new_myitem_hairetu,$syo_temp;
	}
	if ($kensa_flag != 1){
		open(OUT,"< ./dat_dir/prezento.cgi") || &error("プレゼントリストが開けません");
		eval{ flock (OUT, 2); };
		@prezento =<OUT>;
		close(OUT);
		foreach (@prezento){
			&syouhin_sprit ($_);
			if ($syo_hinmoku eq 'クーポン'){
				$kensa_flag = 1;
				$syo_syubetu = 'ギフト';
				$syo_taikyuu = $coupointo;
				$syo_kounyuubi = time;
				$tanka = 0;
				&syouhin_temp;
				push @new_myitem_hairetu,$syo_temp;
				last;
			}
		}
		if ($kensa_flag != 1){&error("クーポンの取り扱いありません");}
	}
	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
	#データ更新
&temp_routin;
&log_kousin($my_log_file,$k_temp);
	#自分の所有物ファイルを更新
	open(OUT,">$monokiroku_file") || &error("Write Error : $monokiroku_file");
	eval{ flock (OUT, 2); };
	print OUT @new_myitem_hairetu;
	close(OUT);	
}

1;
