# -*- coding: utf-8 -*-
from mahjong.hand_calculating.hand_config import HandConfig


class ScoresCalculator(object):

    def calculate_scores(self, han, fu, config, is_yakuman=False):
        """
        Calculate how much scores cost a hand with given han and fu
        :param han: int
        :param fu: int
        :param config: HandConfig object
        :param is_yakuman: boolean
        :return: a dictionary with main and additional cost
        for ron additional cost is always = 0
        for tsumo main cost is cost for dealer and additional is cost for player
        {'main': 1000, 'additional': 0}
        """

        # kazoe hand
        if han >= 13 and not is_yakuman:
            # Hands over 26+ han don't count as double yakuman
            if config.options.kazoe_limit == HandConfig.KAZOE_LIMITED:
                han = 13
            # Hands over 13+ is a sanbaiman
            elif config.options.kazoe_limit == HandConfig.KAZOE_SANBAIMAN:
                han = 12

        if han >= 5:
            if han >= 78:
                if config.options.limit_to_sextuple_yakuman:
                    rounded = 48000
                else:
                    extra_han, _ = divmod(han-78, 13)
                    rounded = 48000 + (extra_han * 8000)
            elif han >= 65:
                rounded = 40000
            elif han >= 52:
                rounded = 32000
            elif han >= 39:
                rounded = 24000
            # double yakuman
            elif han >= 26:
                rounded = 16000
            # yakuman
            elif han >= 13:
                rounded = 8000
            # sanbaiman
            elif han >= 11:
                rounded = 6000
            # baiman
            elif han >= 8:
                rounded = 4000
            # haneman
            elif han >= 6:
                rounded = 3000
            else:
                rounded = 2000

            double_rounded = rounded * 2
            four_rounded = double_rounded * 2
            six_rounded = double_rounded * 3
        else:
            base_points = fu * pow(2, 2 + han)
            rounded = (base_points + 99) // 100 * 100
            double_rounded = (2 * base_points + 99) // 100 * 100
            four_rounded = (4 * base_points + 99) // 100 * 100
            six_rounded = (6 * base_points + 99) // 100 * 100

            is_kiriage = False
            if config.options.kiriage:
                if han == 4 and fu == 30:
                    is_kiriage = True
                if han == 3 and fu == 60:
                    is_kiriage = True

            # mangan
            if rounded > 2000 or is_kiriage:
                rounded = 2000
                double_rounded = rounded * 2
                four_rounded = double_rounded * 2
                six_rounded = double_rounded * 3

        if config.is_tsumo:
            return {'main': double_rounded, 'additional': config.is_dealer and double_rounded or rounded}
        else:
            return {'main': config.is_dealer and six_rounded or four_rounded, 'additional': 0}


class Aotenjou(ScoresCalculator):

    def calculate_scores(self, han, fu, config, is_yakuman=False):

        base_points = fu * pow(2, 2 + han)
        rounded = (base_points + 99) // 100 * 100
        double_rounded = (2 * base_points + 99) // 100 * 100
        four_rounded = (4 * base_points + 99) // 100 * 100
        six_rounded = (6 * base_points + 99) // 100 * 100

        if config.is_tsumo:
            return {'main': double_rounded, 'additional': config.is_dealer and double_rounded or rounded}
        else:
            return {'main': config.is_dealer and six_rounded or four_rounded, 'additional': 0}

    def aotenjou_filter_yaku(self, hand_yaku, config):
        #print ("")
        #print (hand_yaku)

        # in aotenjou yakumans are normal yaku
        # but we need to filter lower yaku that are precursors to yakumans
        if config.yaku.daisangen in hand_yaku:
            # for daisangen precursors are all dragons and shosangen
            hand_yaku.remove(config.yaku.chun)
            hand_yaku.remove(config.yaku.hatsu)
            hand_yaku.remove(config.yaku.haku)
            hand_yaku.remove(config.yaku.shosangen)

        if config.yaku.tsuisou in hand_yaku:
            # for tsuuiisou we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.shosuushi in hand_yaku:
            # for shosuushi we do not need to remove anything
            pass

        if config.yaku.daisuushi in hand_yaku:
            # for daisuushi we need to remove toitoi
            hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.suuankou in hand_yaku or config.yaku.suuankou_tanki in hand_yaku:
            # for suu ankou we need to remove toitoi and sanankou (sanankou is already removed by default)
            if config.yaku.toitoi in hand_yaku:
                # toitoi is "optional" in closed suukantsu, maybe a bug? or toitoi is not given when it's kans?
                hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chinroto in hand_yaku:
            # for chinroto we need to remove toitoi and honroto
            hand_yaku.remove(config.yaku.toitoi)
            hand_yaku.remove(config.yaku.honroto)

        if config.yaku.suukantsu in hand_yaku:
            # for suukantsu we need to remove toitoi and sankantsu (sankantsu is already removed by default)
            if config.yaku.toitoi in hand_yaku:
                # same as above?
                hand_yaku.remove(config.yaku.toitoi)

        if config.yaku.chuuren_poutou in hand_yaku or config.yaku.daburu_chuuren_poutou in hand_yaku:
            # for chuuren poutou we need to remove chinitsu
            hand_yaku.remove(config.yaku.chinitsu)

        if config.yaku.daisharin in hand_yaku:
            # for daisharin we need to remove chinitsu, pinfu, tanyao, ryanpeiko, chiitoitsu
            hand_yaku.remove(config.yaku.chinitsu)
            if config.yaku.pinfu in hand_yaku:
                hand_yaku.remove(config.yaku.pinfu)
            hand_yaku.remove(config.yaku.tanyao)
            if config.yaku.ryanpeiko in hand_yaku:
                hand_yaku.remove(config.yaku.ryanpeiko)
            if config.yaku.chiitoitsu in hand_yaku:
                hand_yaku.remove(config.yaku.chiitoitsu)

        if config.yaku.ryuisou in hand_yaku:
            # for ryuisou we need to remove honitsu, if it is there
            if config.yaku.honitsu in hand_yaku:
                hand_yaku.remove(config.yaku.honitsu)

        # print(hand_yaku)
