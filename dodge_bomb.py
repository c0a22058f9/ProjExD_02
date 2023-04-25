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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect() # こうかとんのSurfaceに対するrectのSurfaceを取得
    kk_rect.center = 900,400 # こうかとんの座標の中央を900, 400に設定
    tmr = 0

    bb_img = pg.Surface((20,20)) # 爆弾のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) # 爆弾を作成
    bb_img.set_colorkey((0,0,0))  # 爆弾の余白を透明化
    x, y = random.randint(0,1600), random.randint(0,900) # 爆弾のランダムな座標を取得し、x, yに代入
    screen.blit(bb_img, [x, y]) # 爆弾を表示
    vx,vy = +1, +1 # 爆弾の移動用座標を作成
    bb_rect = bb_img.get_rect() # 爆弾のSurfaceに対するrectのSurfaceを取得
    bb_rect.center = x, y # 爆弾の中心座標をx, yに設定

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed() # 矢印キーの入力を受け付ける
        for k, mv in delta.items(): # 辞書deltaのkeyとvalueをk, mvに入れる
            if key_lst[k]: # 矢印キーの入力を受けたとき
                kk_rect.move_ip(mv) # こうかとんの座標を移動

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)
        
        bb_rect.move_ip(vx, vy) # 爆弾の座標を移動
        screen.blit(bb_img, bb_rect) #  爆弾を移動後の座標に表示

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()