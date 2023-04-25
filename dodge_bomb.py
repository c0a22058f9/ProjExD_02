import random
import sys

import pygame as pg


# こうかとんの移動量を表す辞書
delta = {
        pg.K_UP: (0, -1), # 上の移動量
        pg.K_DOWN: (0, +1), # 下の移動量
        pg.K_LEFT: (-1, 0), # 左の移動量
        pg.K_RIGHT: (+1, 0) # 右の移動量
        }
kk_img = pg.image.load("ex02/fig/3.png")
delta_kk_img = {  
            (0, -1):pg.transform.rotozoom(pg.transform.flip(kk_img,True,False), 90, 2.0),
            (+1, -1):pg.transform.rotozoom(pg.transform.flip(kk_img,True,False), 45, 2.0),
            (+1, 0):pg.transform.rotozoom(pg.transform.flip(kk_img,True,False), 0, 2.0),
            (+1, +1):pg.transform.rotozoom(pg.transform.flip(kk_img,True,False), -45, 2.0),
            (0, +1):pg.transform.rotozoom(pg.transform.flip(kk_img,True,False), -90, 2.0),
            (-1, +1):pg.transform.rotozoom(kk_img, -45, 2.0),
            (-1, 0):pg.transform.rotozoom(kk_img, 0, 2.0),
            (-1, -1):pg.transform.rotozoom(kk_img, 45, 2.0)
            }

bb_imgs = []
accs = [a for a in range(1,11)]
for r in range(1,11):
    bb_img = pg.Surface((20*r, 20*r))
    pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    bb_imgs.append(bb_img)


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool,bool]:
    """
    obj_rctがscr_rct内or外にあるのかを判定し、真理値タプルを返す関数
    引数１：画面Surfaceのrect
    引数２：オブジェクトのSurfaceのrect
    戻り値：横方向、縦方向のはみだし判定結果（画面内：True/画面外：False）
    """
    yoko, tate = True, True

    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = False

    return yoko, tate
    

    


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("ex02/fig/3.png"), 0, 2.0)
    # kk_img_left = kk_img
    # kk_img_right = pg.transform.flip(kk_img,True,False)
    kk_rct = kk_img.get_rect() # こうかとんのSurfaceに対するrectのSurfaceを取得
    kk_rct.center = 900,400 # こうかとんの座標の中央を900, 400に設定
    tmr = 0

    bb_img = pg.Surface((20,20)) # 爆弾のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) # 爆弾を作成
    bb_img.set_colorkey((0,0,0))  # 爆弾の余白を透明化
    x, y = random.randint(0,1600), random.randint(0,900) # 爆弾のランダムな座標を取得し、x, yに代入
    screen.blit(bb_img, [x, y]) # 爆弾を表示
    vx,vy = +1, +1 # 爆弾の移動用座標を作成
    bb_rct = bb_img.get_rect() # 爆弾のSurfaceに対するrectのSurfaceを取得
    bb_rct.center = x, y # 爆弾の中心座標をx, yに設定
    avx, avy = vx*accs[min(tmr//1000, 9)], vy*accs[min(tmr//1000, 9)]
    bb_img = bb_imgs[min(tmr//1000, 9)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed() # 矢印キーの入力を受け付ける
        for k, mv in delta.items(): # 辞書deltaのkeyとvalueをk, mvに入れる
            if key_lst[k]: # 矢印キーの入力を受けたとき
                kk_rct.move_ip(mv) # こうかとんの座標を移動
                for ke, val in delta_kk_img.items():
                    if mv == ke:
                        kk_img = delta_kk_img[ke]
        
        if check_bound(screen.get_rect(), kk_rct) != (True, True): # 画面内外判定
            for k, mv in delta.items(): # 辞書deltaのkeyとvalueをk, mvに入れる
                if key_lst[k]: # 矢印キーの入力を受けたとき
                    kk_rct.move_ip(-mv[0], -mv[1]) # こうかとんの座標を移動。ひとつ前の値を入れたいため、それぞれ-mv[0], -mv[1]に設定


        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(vx, vy) # 爆弾の座標を移動
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko: # 横方向にはみ出ていたら
            vx *= -1 # 横方向の移動を反転
        if not tate: # 縦方向にはみ出ていたら
            vy *= -1 # 縦方向の移動を反転
        screen.blit(bb_img, bb_rct) #  爆弾を移動後の座標に表示
        if kk_rct.colliderect(bb_rct): # こうかとんと爆弾の衝突判定
            return  # 衝突していたら、終了

        avx, avy = vx*accs[min(tmr//1000, 9)], vy*accs[min(tmr//1000, 9)]
        bb_img = bb_imgs[min(tmr//1000, 9)]
        bb_img.set_colorkey((0,0,0))

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()