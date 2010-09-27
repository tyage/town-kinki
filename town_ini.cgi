#------------------以下、初期設定項目-------------------
#街の名前
my @titles = ("近畿地方","ウホッキンキチホウホッ","キンキチホー");
my $no = int(rand(3));
$title=$titles[$no];
#サブタイトル
$subtitle=$titles[$no].'　―　ABCオロチ ver';

#管理者名（ここで設定した管理者名とパスワードで新規登録することで、家を無料で作成することができます）
$admin_name = '';
#管理者パスワード
$admin_pass = '';
#副管理者パスワード
$admin_pass2 = '';

#プロキシー強化および自分以外が進入防止　town_maker.cgi　のホスト強化 koko2007/09/09
$host_kyuka = 'yes';
#プロキシー強化　town_maker.cgi　
$host_kyuka_meker = 'no';

# アクセス制限許可型（半角スペースで区切る）
#  → 許可するホスト名又はIPアドレスを記述 優先度一番（アスタリスク可）これを使うと下記は無視されます。
#  → 記述例 $denyHost = '*.anonymizer.com 211.154.120.* local*';半角スペース区切り
$okhost = '*';
#管理者ホスト名1　'abc.def.ne.jp'のような自分のアクセスポイントを入れる。
$my_host1 = '*.zaq.ne.jp';
#管理者ホスト名2　　同上　会社などの出先 書かれていなければ普通通り。
$my_host2 = '*.eonet.ne.jp';

#戻り先ホームページ
$homepage = 'http://w2.oroti.com/~tyage/';
#管理者メールアドレス（問い合わせ用）
$master_ad = 'tyage2@nifmail.jp';

#メンテ中フラグ（通常は0。1でメンテ中となりゲームを中断させることができます）
$mente_flag = '0';
#メンテナンス時のメッセージ
$mente_message = 'メンテナンス中です。ちょっと待っててね。';

# 税金徴収　''=無し　　'1～28'=日にち指定　　'Sun','Mon','Tue','Wed','Thu','Fri','Sat'=曜日指定
$zeikin_shitei = 'Mon';

#画像フォルダー（img）の指定。プログラムからの相対パス or http://～から始まる絶対パス　※最後の「/」は不要です。
$img_dir = './img';

#トップ画面でのお知らせ内容（タグ可）
$osirase = <<"EOM";
<font color=#666666>
	あんたも「新規登録」から登録して、この地方の住民になってみまへんか？<br>
	ここでは掲示板やゲームなどを通して色々な方と知りあえるで。<br>
	いろんな職業についたり、けったいな家を建てたり、どんな人生にするかはあんた次第や！
</font>
EOM

#作成する街の名前
@town_hairetu = ("京阪神ストリート","近江レイク","奈良シティ","和歌山アイランド");
#街の地価（上で指定した街の地価。左から順に上と対応させる。単位は万円）
@town_tika_hairetu = ("5000","2000","1000","500");
#街の背景スタイル（上で指定した街の背景スタイル設定。左から順に上と対応させる。スタイルで画像指定可）
@page_back = ("background-color:#afeeee","background-color:#7D7DFF","background-color:#99cc66","background-color:#cccc99","background-color:#008000");

#参加者が建てられる家の画像と価格（'画像名','価格'の形で設定してください。価格の単位は（万円）です。家の画像はimgフォルダに入れておく必要があります。）
%ie_hash=('house/kamakura.gif','50','house/bil6.gif','5000','house/bil7.gif','5000','house/bil8.gif','5000','house/bil9.gif','5000','house/house_y.gif','150','house/house_p.gif','150','house/house_o.gif','150','house/house_w.gif','150','house/house_b.gif','150','house/house_r.gif','150','house/house_1.gif','160','house/house_2.gif','160','house/house_3.gif','170','house/house_4.gif','180','house/house_5.gif','180','house/house_6.gif','180','house/house_7.gif','190','house/house_8.gif','200','house/house_9.gif','200','house/house_10.gif','200','house/house_11.gif','500','house/house_12.gif','500','house/house_13.gif','500','house/house_14.gif','1000','house/house_15.gif','1000','house/house_16.gif','1000','house/house_17.gif','300','house/house_18.gif','300','house/house_19.gif','300','house/house_20.gif','400','house/house_21.gif','400','house/house_22.gif','400','house/house_23.gif','500','house/house_24.gif','500','house/house_25.gif','100','house/house_26.gif','400','house/house_27.gif','400','house/house_28.gif','400','house/house_29.gif','500','house/house_30.gif','600','house/house_31.gif','300','house/house_32.gif','300','house/house_33.gif','200','house/house_34.gif','200','house/house_35.gif','100','house/house_36.gif','100','house/house_37.gif','100','house/house_38.gif','500','house/house_39.gif','500','house/house_40.gif','2500','house/house_41.gif','1000','house/houseL_1.gif','2000','house/houseR_1.gif','2000','house/houseL_2.gif','2200','house/houseR_2.gif','2200','house/houseL_3.gif','2400','house/houseR_3.gif','2400','house/houseL_4.gif','2600','house/houseR_4.gif','2600','house/houseT_1.gif','2800','house/houseB_1.gif','2800','house/houseT_2.gif','15','house/houseB_2.gif','15','house/houseT_3.gif','1111','house/houseB_3.gif','1111','house/castle1.gif','3000','house/castle2.gif','3000','house/castle3.gif','3000','house/castle4.gif','3000','house/castle5.gif','5000000000000','house/castle6.gif','5000000000000','house/castle7.gif','5000000000000','house/castle8.gif','5000000000000','house/parliament_r.gif',10000,'house/parliament_l.gif',10000,'house/kinkaku.gif',1000000,'house/kinkaku2.gif',10000000,'house/statue.gif',1000,'house/sunshine.gif',1000000,'house/clock.gif',100000,'house/clock2.gif',100000);
#内装費用（左からA～Dランク。Aランクは４つのコンテンツを表示可能、Dランクは１つのみのコンテンツを表示可能。単位は万円）
@housu_nedan = ("1200","800","400","100");

#役場でのランキング表示数
$rankMax='50';

#何日間食事しないと死んでしまうか（ユーザー削除期間）
$deleteUser = '3000';
#食事は何分ごとにとることができるか
$syokuzi_kankaku = '60';

#身体パワーの回復率（何秒で１ポイント回復するか。数が少ないほど回復が早い）
$sintai_kaihuku = "10";
#頭脳パワーの回復率（何秒で１ポイント回復するか。数が少ないほど回復が早い）
$zunou_kaihuku = "10";

#卸問屋に並べる商品の数
$orosi_sinakazu = "120";
#卸問屋の在庫調整（「syouhin.cgi」で指定の在庫の何倍の数を置くか。お店が増えてきて問屋の在庫数が足らないと思ったらこの数字を増やす。）
$ton_zaiko_tyousei = '2';
#食堂やデパートでの在庫調節値（基準の在庫数をこの数字で割った数が店頭に並びますので、この数字を大きくするほど在庫が少なく、小さくするほど在庫が多くなります）
$zaiko_tyousetuti ="1";

#セントラル食堂に並べる食品の種類数
$syokudou_sinakazu = "30";
#デパートに並べる商品の種類数
$depart_sinakazu = "110";

#所有物の限度数
$syoyuu_gendosuu = '25';

#お店の種別（このゲーム内のお店に出回る商品のデータは、「dat_dir」内にある「shouhin.cgi」に記録されています。「shouhin.cgi」ファイルの一番左にあるのが商品種別で、ここの「お店の種別」と対応している必要があります。※ただし食堂を表す「食」は「shouhin.cgi」のみにある種別となります）
@global_syouhin_syubetu = ("スーパー","書籍","食料品","薬","スポーツ用品","電化製品","美容","アダルト","DVD","ファーストフード","日用品","お花","デザート","ギフト","アルコール","ゲーム","ドリンク","秘密の商品","関西名産店","東北名産店","ペット","合成");

#挨拶ログの保存件数
$aisatu_max = '100';

#最大登録者数
$saidai_ninzuu = '150';

#自動ファイル生成フォルダのパーミッション（777＝1、755＝2）※1でエラーが出るようなら2を試してみてください。
$zidouseisei = "1";

#ステータス窓の枠色
$st_win_wak = "#339966";
#ステータス窓の背景色
$st_win_back = "#ffffff";

#設置する掲示板（'掲示板の名前'を「,」でつないだ形で設定してください。ここでの名前はマウスをのせた時にウインドウに表示させる名前です。ページ内のタイトルや各種デザイン・設定は管理メニューの「管理者作成BBSの設定」で行います。実際に街の任意の位置へ掲示板を配置するのは、管理者メニューの「街のレイアウト作成」で行ってください。）
@admin_bbs_syurui =('みんなの広場。総合掲示板です。','疑問解決BBS。普段疑問に思っている事を聞いてしまおう。','オススメ情報BBS。あなたのお薦め教えてください。','ハッピー掲示板。あなたのシアワセを感じる瞬間を投稿してください。','意見掲示板。あなたの意見をください。（欲しい施設など）','京阪神ストリート住民専用掲示板','近江レイク住民専用掲示板','奈良シティ住民専用掲示板','和歌山アイランド住民専用掲示板');

#上記掲示板の画像（左から上と対応させる）
@admin_bbs_gazou =('bbs1.gif','bbs2.gif','bbs3.gif','bbs4.gif','bbs5.gif','bbs6.gif','bbs6.gif','bbs6.gif','bbs6.gif');

#BBSの保存記事数（親記事、レス記事合わせた件数です）
$bbs_kizi_max = '100';

# アクセス拒否するホスト名
@deny = ("*.host.xx.jp","xxx.xxx.xx.");
#多重登録禁止（1で禁止、0で禁止しない）
$tajuukinsi_flag = '1';
#多重登録者をログインできなくする（1でする、0でしない）
$tajuukinsi_deny = '1';

#Ｃリーグ１大会の日数
$c_nissuu = '14';
#Ｃリーグの試合数
$c_siaisuu = "100";
#Ｃリーグの試合間隔（単位は分）
$c_siai_kankaku = '1';

#キャラクターの画像サイズ指定（指定しない場合、自由サイズになります）
$chara_x_size = '32';	#横サイズ
$chara_y_size = '32';	#縦サイズ

#週間街コンテストの賞金額（単位は万円）
$mati_con_syoukin = '300';

#街コンテストの日数
$mati_con_nissuu = '7';

#プロフィールの１ページ表示数
$hyouzi_max_grobal = '10';

##以下、プロフィールでの選択肢
#性別のselect
		@sex_array=('','男','女','中間');

#年齢のselect
		@age_array=('','～14歳','15～18歳','19～22歳','23～26歳','27～30歳','31～34歳','35～38歳','39～42歳','43～46歳','47～50歳','51歳～');

#住所のselect
		@address_array=('','北海道','青森','岩手','宮城','秋田','山形','福島','群馬','栃木','茨城','埼玉','千葉','東京','神奈川','新潟','富山','石川','福井','山梨','長野','岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄','海外');
		
#選択式プロフィール項目1
		$prof_name1='アピールポイント';
		@prof_array1=('','かっこいい','頭がいい','背が高い','ガッシリ体格','マッチョ','優しい','お金持ち','車が自慢','一人暮らし','心意気','素直','マメ','誠実','面白い','カワイイ','キレイ','胸が自慢','脚が自慢','ナイスバディ','家庭的','スポーツ得意','歌がうまい','料理が得意','エッチ','ダメ人間');

#選択式プロフィール項目2
		$prof_name2='ただいま';
		@prof_array2=('','恋人募集中','友だち募集中','メル友募集中','趣味友募集中','飲み友募集中','合コン仲間募集中','ＨＰ宣伝中','不倫相手募集中','愛人募集中','仕事一筋中','新婚中','別居中','不倫中','熱愛中','同棲中','勘当中','家出中','平凡生活中','片思い中');

#選択式プロフィール項目3
		$prof_name3='身長';
		@prof_array3=('','秘密','低い','やや低い','普通','やや高い','高い');

#選択式プロフィール項目4
		$prof_name4='体重';
		@prof_array4=('','秘密','やせてる','少しやせてる','普通','ややぽちゃ','ぽちゃ');

#選択式プロフィール項目5
		$prof_name5='職業';
		@prof_array5=('','フリーター','学生','無職','ＯＬ','サラリーマン','公務員','主婦','営業マン','技術職','商社マン','銀行マン','SE・プログラマー','パイロット','スチュワーデス','警察','消防士','僧侶','ファッション関係','プランナー','編集者','クリエイター','販売員','美容師','大工','マスコミ','社長','会社役員','事務職','コンピュータ','飲食業','教師','医師','アーティスト','デザイナー','タレント','看護婦','保母','コンサルタント','自営業','水商売','音楽関係','芸人','スポーツ選手','その他');
		
#記述式プロフィール項目
	@kijutu_prof = ('似ている有名人','趣味','ホームページ','弱点','好きな有名人','好きなスポーツ','好きな映画','好きなＴＶ番組','好きな音楽','好きな異性のタイプ','将来の夢','嫌いなもの','今一番行きたいところ','今一番したいこと','一言コメント');

##以下各種デザインのスタイル設定
#メッセージ窓のスタイル設定
$message_win ="border: #0000ff; border-style: dotted; border-top-width: 1px; border-right-width: 1px; border-bottom-width: 1px; border-left-width: 1px; background-color:#ffffff; color:000000";

##########################ver.1.1追加
#ギフト所有限度数（贈られたギフト）
$gift_gendo = '10';

#ギフト購入限度数
$kounyu_gift_gendo = '10';

#自分のお店に置ける商品アイテム数
$mise_zaiko_gendo = '100';

#アイテム数が限度以上なら同じアイテムでも在庫を増やせなくする（増やせない＝1、増やせる＝0）
$douitem_ok = '0';

#温泉入浴時に通常の何倍の早さでパワーが回復するか
$onsen_times = '10';

#温泉で使っている画像の数（温泉の画像を追加する場合、img/onsenフォルダー内に○.jpg（○は1から始まる連番の数字）というファイル名で入れてください）
$on_gazou_suu = '10';

#温泉入浴料（単位は円）
$nyuuyokuryou = '500';

#gzipのパス（サーバーがgzip圧縮に対応していない場合空欄にしてください（※画面が真っ白になる場合などは対応してない可能性が高いです）。ただし、gzip圧縮が使えるとテキストの転送量をかなり小さくできます）
$gzip = '';

#徒歩で街の移動にかかる時間（秒指定）
$matiidou_time = '10';

#各乗り物ごとで移動にかかる時間（'乗り物','かかる秒数'のフォーマットで。乗り物はsyouhin.cgiにある商品でないと意味がありません。ただし商品種別が「乗り物」である必要はありません。コメントに「※移動手段です」と入れてあげた方が親切かと思います。また速いものから先に並べてください）
%idou_syudan =('ローラースルーゴーゴー','20','ベスパ','10','スーパーカブ','10','ドゥカティ','7','ナナハン','7','カローラ','7','ボルボ','6','キャデラック','6','ベンツ','5','ロールスロイス','5','スカイラインGTR','4','ロータスヨーロッパ','4','アルファロメオ','4','ジャガー','4','BMW','4','フェアレディZ','5','自転車','15','ポルシェ','3','フェラーリ','2','ミグ25','0');

#街移動時に事故を起こす確率（何分の一の確率かで指定。デフォルトでは10分の１という意味）
$ziko_kakuritu = '10';

#行動制限時間（秒指定。制限を付けない場合＝0）
$koudou_seigen = '5';

#カードゲームができる間隔（単位：分）
$crad_game_time = '10';

##########################ver.1.2追加

#同一アイテムの所有個数の限度
$item_kosuuseigen = '5';

#仕事ができる間隔（単位：分。制限無しの場合は0を指定）
$work_seigen_time = '5';

#競馬の購入限度枚数（単位：枚）
$keiba_gendomaisuu = '200';

##########################ver.1.21追加
#メンバーログのファイルロック方式（0でリネームロック、0でうまく稼働しない場合1にしてください）
$mem_lock_num = '0';


##########################ver.1.3追加
#恋人斡旋プロフィール記録ファイル
$as_profile_file='./log_dir/as_pfofilelog.cgi';
#カップル記録ファイル
$couple_file='./log_dir/couplelog.cgi';
#子供記録ファイル
$kodomo_file='./log_dir/kodomolog.cgi';
#街ニュース記録ファイル
$news_file='./log_dir/mati_news.cgi';

#役場のニュース表示件数
$news_kensuu = '100';

#お店に置いておける在庫の上限数
$mise_zaiko_limit = '100';

#メールの保存件数
$mail_hozon_gandosuu = '50';

#特別風呂は何倍の速度で回復するか
$tokubetu_times = '100';
#特別風呂でかかる費用（円）
$tokubetuburo_hiyou = '5000';
#松風呂は何倍の速度で回復するか
$matu_times = '1000';
#松風呂でかかる費用（円）
$matu_hiyou = '50000';
#竹風呂は何倍の速度で回復するか
$take_times = '400';
#竹風呂でかかる費用（円）
$take_hiyou = '20000';
#梅風呂は何倍の速度で回復するか
$ume_times = '200';
#梅風呂でかかる費用（円）
$ume_hiyou = '10000';
#銅風呂は何倍の速度で回復するか
$dou_times = '2500';
#銅風呂でかかる費用（円）
$dou_hiyou = '50000';
#銀風呂は何倍の速度で回復するか
$gin_times = '5000';
#銀風呂でかかる費用（円）
$gin_hiyou = '100000';
#金風呂は何倍の速度で回復するか
$kin_times = '10000';
#金風呂でかかる費用（円）
$kin_hiyou = '1000000';

#恋愛システムを使うか（1＝使う、0＝使わない　※0にすることでハート＆子供アイコンが出現されなくなります。また、0の場合「恋人斡旋所」も街に設置しないでください）
$renai_system_on = '1';
#恋愛に必要なLOVEパラメータの数値
$need_love = '200';
#同性の恋愛を許可する（許可しない＝0、許可する＝1）
$douseiai_per = '1';
#同時に何人とつきあえるか（配偶者＋恋人）
$koibito_seigen = '5';
#結婚に必要なラブラブ度（思い出数値の合計）
$aijou_kijun = '500';
#結婚に必要な思い出数値（それぞれの思い出の最低値）
$omoide_kijun = '80';
#恋人と何日間デートをしないと別れてしまうか
$wakare_limit_koibito = '10';
#配偶者と何日間デートをしないと別れてしまう
$wakare_limit_haiguu = '30';
#相手が配偶者の場合の子供ができる確率（10なら10分の１の確率）
$kodomo_kakuritu1 = '5';
#相手が恋人の場合の子供ができる確率（80なら80分の１の確率）
$kodomo_kakuritu2 = '10';
#子育てできる間隔（単位：時間）
$kosodate_kankaku = '3';
#子供のパラメータを１あげるのにかかる費用（円）
$youikuhiyou = '20000';
#何日間子供に食事を与えないと死んでしまうか
$kodomo_sibou_time = '7';
#子供は何歳まで生きるか（仕送りが送られてくる期間）
$kodomo_sibou_time2 = '40';
#以下、結婚斡旋所での変更可能なプロフィール項目
	#年齢のselect
		@as_age_array=('','～14歳','15～18歳','19～22歳','23～26歳','27～30歳','31～34歳','35～38歳','39～42歳','43～46歳','47～50歳','51歳～');
	#住所のselect
		@as_address_array=('','北海道','青森','岩手','宮城','秋田','山形','福島','群馬','栃木','茨城','埼玉','千葉','東京','神奈川','新潟','富山','石川','福井','山梨','長野','岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄','海外');

	#選択式プロフィール項目1
		$as_prof_name2='アピールポイント';
		@as_prof_array2=('','かっこいい','頭がいい','背が高い','ガッシリ体格','マッチョ','優しい','お金持ち','車が自慢','一人暮らし','心意気','素直','マメ','誠実','面白い','カワイイ','キレイ','胸が自慢','脚が自慢','ナイスバディ','家庭的','スポーツ得意','歌がうまい','料理が得意','エッチ','ダメ人間');

	#選択式プロフィール項目2
		$as_prof_name3='住んでいる街';
		@as_prof_array3=('','家を持っていない','メインストリート','シーリゾート','カントリータウン','ダウンタウン');

	#選択式プロフィール項目3
		$as_prof_name4='欲しい子供の数';
		@as_prof_array4=('','子供はいらない','1人でいい','2人くらい','3人くらい','4、5人は欲しい','6人以上');

	#選択式プロフィール項目4
		$as_prof_name5='相手の年齢は';
		@as_prof_array5=('','年齢は気にしない','同じくらいがいい','年上がいい','年下がいい','すごく年上がいい','すごく年下がいい');

	#選択式プロフィール項目5
		$as_prof_name6='相手に望むこと';
		@as_prof_array6=('','かっこよさ','頭のよさ','背の高さ','ガッシリ体格','マッチョ','優しさ','裕福度','一人暮らし','心意気','素直さ','マメさ','誠実さ','面白さ','カワイさ','キレイさ','胸の大きさ','脚のキレイさ','ナイスバディ','家庭的','スポーツマン','歌のうまさ','料理の上手さ','エッチさ');

#街の下に挨拶を表示するか（表示する＝1、表示しない＝0）
$top_aisatu_hyouzi = '1'; #koko
#上で表示するにした場合の表示件数
$top_aisatu_hyouzikensuu = '20';
#上で表示するにした場合の名前の色
$top_aisatu_hyouzi_iro1 = '#333399';
#上で表示するにした場合の記事の色
$top_aisatu_hyouzi_iro2 = '#333333';

#トップページで街の下に自由表示するするhtml（EOM～EOMの間にhtmlで記述）
$top_information = <<"EOM";
<style type="text/css"><!--
	#menu{
		cursor:pointer;
		border: 1px #199eff solid;
		border-width: 2px 2px 0px 2px;
		background-color: #eeeeee;
		width: 30%;
	}
	#menu2{
		cursor:pointer;
		border: 1px #199eff solid;
		border-width: 0px 2px 2px 2px;
		background-color: #eeeeee;
		width: 30%;
	}
 --></style>
<Script Language="JavaScript"><!--
	function Change(place){
		place.style.backgroundColor='#199eff';
		place.style.color='#ffffff';
	}
	function Back(place){
		place.style.backgroundColor='';
		place.style.color='';
	}
		
	function menu(ima,tugi){
		if(document.all){
			document.all(ima).style.position = "absolute";
			document.all(ima).style.display = "none";
			document.all(tugi).style.position = "static";
			document.all(tugi).style.display = "block";
		}else if(document.getElementById){
			document.getElementById(ima).style.position = "absolute";
			document.getElementById(ima).style.display = "none";
			document.getElementById(tugi).style.position = "static";
			document.getElementById(tugi).style.display = "block";
		}
	}
//--></script>

<center>

<a href="town_maker.cgi?town_no=0">京阪神ストリート</a>　｜　
<a href="town_maker.cgi?town_no=1">近江レイク</a>　｜　
<a href="town_maker.cgi?town_no=2">奈良シティ</a>　｜　
<a href="town_maker.cgi?town_no=3">和歌山アイランド</a>

<br><br>

<div id="image">
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td bgcolor='#199eff'><font color='#ffffff'><b>画像の著作権</b></font></td>
<td> </td>
<td onclick="menu('image','link')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>リンク</b></td>
<td> </td>
<td onclick="menu('image','black')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>ブラックリスト</b></td>
</tr></table>

<table border="1" bordercolor="#199eff" bgcolor="#ffffff" width="100%" cellpadding="3" cellspacing="0">
<tr align="center">
<td><a href="http://momo-kitty.hp.infoseek.co.jp/" target="_blank"><img src="img/bana/kitty.gif" border="0"></a></td>
<td><a href="http://kei.cside.tv/" target="_blank"><img src="img/bana/guutara.gif" border="0"></a></td>
<td><a href="http://lll32x32iconlll.nobody.jp/" target="_blank"><img src="img/bana/32x32.gif" border="0"></a></td>
<td><a href="http://homepage3.nifty.com/diu/" target="_blank"><img src="img/bana/yorozu.gif" border="0"></a></td>
</tr>
<tr align="center">
<td><a href="http://zangoe.fc2web.com" target="_blank"><b>office118</b></a></td>
<td><a href="http://www.qoonet.com/hakoniwa.html" target="_blank"><b>箱庭ＱｏｏＬａｎｄ</b></a></td>
<td><a href="http://pina-kingdom.hp.infoseek.co.jp/" target="_blank"><b>PINACOLADA KINGDOM</b></a></td>
<td><a href="http://oab.sytes.net:4600/~flower/" target="_blank"><img src="img/bana/milk.gif" border="0"></a></td>
</tr>
<tr align="center">
<td><a href="http://pata-anime.jp/index.html" target="_blank"><img src="img/bana/pataani.gif" border="0"></a></td>
<td><a href="http://homepage1.nifty.com/piyo/" target="_blank"><img src="img/bana/piyo.gif" border="0"></a></td>
<td><a href="http://ayfreenet.web.infoseek.co.jp/" target="_blank"><img src="img/bana/garo.gif" border="0"></a></td>
<td><b>黄昏のピヨ様（住民）</b></td>
</tr>
</table>

</div>

<div id="link" style="position:absolute;display:none;">
<table width="100%" cellspacing="0" cellpadding="5" ><tr align="center">
<td onclick="menu('link','image')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>画像の著作権</b></td>
<td> </td>
<td bgcolor='#199eff'><font color='#ffffff'><b>リンク</b></font></td>
<td> </td>
<td onclick="menu('link','black')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>ブラックリスト</b></td>
</tr></table>

<table border="1" bordercolor="#199eff" bgcolor="#ffffff" width="100%" cellpadding="3" cellspacing="0">
<tr>
<td>
<a href="./manual.html" target="_blank" onMouseOver="Navi('$img_dir/about.gif', 'マニュアル', '初めての方はごらんください。<br>あまり細かいことは乗っていません。', 0, event);" onMouseOut="NaviClose();"><b><u>初心者への説明</u></b></a><br>
<a href="./kiyaku.html" target="_blank" onMouseOver="Navi('$img_dir/about.gif', '利用規約', 'できるだけ見てください。<br>そこまで厳しくはないと思います。', 0, event);" onMouseOut="NaviClose();"><b><u>利用規約</u></b></a><br>
<br>
<a href="http://town-kaizou.a.orn.jp/" target="_blank" onMouseOver="Navi('$img_dir/about.gif', 'ＴＯＷＮの設置＆改造講座', 'まだ未完成です。<br>これからいろいろ追加する予定です。', 0, event);" onMouseOut="NaviClose();"><b><u>ＴＯＷＮの設置＆改造講座</u></b></a><br>
<a href="../blog/diary.cgi" target="_blank" onMouseOver="Navi('$img_dir/about.gif', '管理人のブログ', '管理人チャゲの日常の出来事やＴＯＷＮについて書いてます。<br>コメントください。', 0, event);" onMouseOut="NaviClose();"><b><u>管理人のブログ</u></b></a><br>
<A href="http://www.seijyuu.com/game/link/in.cgi?kind=town&id=tyage&mode=top" target="_blank" onMouseOver="Navi('$img_dir/about.gif', 'ランキング', 'ランキングです。<br>ＴＯＷＮ内ではお金がもらえます。', 0, event);" onMouseOut="NaviClose();"><b><u>無料ゲーム【TOWN】設置サイトランキング</b></u></A><br>
<br>
<a href="http://w7.oroti.com/~p0dg/farland3/"><b><u>Farland History Ⅱ</u></b></a>
</td>
</tr>
</table>

</div>

<div id="black" style="position:absolute;display:none;">
<table width="100%" cellspacing="0" cellpadding="5"><tr align="center">
<td onclick="menu('black','image')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>画像の著作権</b></td>
<td> </td>
<td onclick="menu('black','link')" onmouseover="return Change(this)" onmouseout="return Back(this)" id="menu"><b>リンク</b></td>
<td> </td>
<td bgcolor='#199eff'><font color='#ffffff'><b>ブラックリスト</b></font></td>
</tr></table>

<table border="1" bordercolor="#199eff" bgcolor="#ffffff" width="100%" cellpadding="3" cellspacing="0">
<tr>
<td>
呂布（不明）：r-123-48-142-71.commufa.jp<br>
sasaca（荒らし）：p3234-ipbfp1303osakakita.osaka.ocn.ne.jp<br>
デスサイズ（お馬鹿）：FL1-125-199-93-140.hrs.mesh.ad.jp
</td>
</tr>
</table>

</div>

<br>
<script type="text/javascript"><!--
siteid = "20081009165254";
navigation_style = "basic-2";
//--></script>
<script type="text/javascript" src="http://www.togethertown.net/townring/navigationbar.js"></script>

</center>
EOM

##########################ver.1.30追加
# 参加者を表示する（1＝表示、0＝表示しない）
$sanka_hyouzi_kinou = '1';

# 参加者の表示位置（1＝上、0＝下）
$sanka_hyouzi_iti = '1';

#同時にログインできる人数
$douzi_login_ninzuu = 30;

##########################ver.1.40追加
# 参加者ファイル（ver.1.30で"./log_dir/guestlog.cgi"だった指定を変更）
$guestfile = "./guestlog_00.cgi";

#ゲームしないでログアウトするまでの時間（秒）
$logout_time = '1200';

#新規登録の受け付け（1＝うけつけない、0＝うけつける）koko
$new_touroku_per = '0';

#名前＆パスワード記録ファイル
$pass_logfile = './log_dir/passlog.cgi';

#自分や配偶者のお店で商品を買えなくする（1＝買えない、0＝買える）
$kaenai_seigen = '0';

############## 追加 ###################
# 買い物制限品名特定品目を持っていないと買えない物を作る
$kyokahin1 = '人生ゲーム';#'コーヒー';変数名変更
$kyokahin2 = 'ブラジャータウン';#
# 制限品目リスト上記商品を持っていないとこの商品は買えなくなる。
@kyokahitsuyou = ('テスト君','テスト');

#######################################
#------------------設定変更ここまで（以下は必要があれば変更してください）
#スクリプトの名前
$script='./town_maker.cgi';
#個人ログデータファイル
$logfile='./log_dir/memberlog.cgi';
#Ｃリーグログデータファイル
$doukyo_logfile='./log_dir/doukyo_log.cgi';
#オリジナル家リストファイル
$ori_ie_list='./log_dir/ori_ie_log.cgi';
#メイン街パラメータ記録ファイル
$maintown_logfile='./log_dir/maintownlog.cgi';
#卸商品記録ファイル
$orosi_logfile='./log_dir/orosilog.cgi';
#今日の食堂メニュー記録ファイル
$syokudou_logfile='./log_dir/syokudoulog.cgi';
#今日のデパートの品揃え記録ファイル
$depart_logfile='./log_dir/departlog.cgi';
#挨拶ログ記録ファイル
$aisatu_logfile='./log_dir/aisatulog.cgi';
#街コンテストログファイル
$maticon_logfile='./log_dir/maticonlog.cgi';
#街コンテスト功労者ログファイル
$kourousya_logfile='./log_dir/kourousyalog.cgi';
#競馬ログファイル
$keiba_logfile='./log_dir/keibalog.cgi';
#競馬ランキングログファイル
$keibarank_logfile='./log_dir/keibaranklog.cgi';
#ロックファイル名
$lockfile = './lock';
#競馬ロックファイル名
$keibalockfile = './lock2';
#プロフィール記録ファイル
$profile_file='./log_dir/pfofilelog.cgi';
#アンケート全部
$enq_all="log_dir/enq_log.cgi";
#オークションログ
$auction_log = "./log_dir/auction_log.cgi";


1;
