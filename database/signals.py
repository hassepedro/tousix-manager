# -*- coding: utf8 -*-
__author__ = 'remy'

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from database.models import Hote, Flux, Stats
from django.db.models import Q

@receiver(post_save, sender=Hote)
def post_save_hote(sender, **kwargs):
    if kwargs['created'] is True:
        db_flux = list()
        db_flux.append(Flux(hote_src=None, hote_dst=kwargs['instance'], type="ICMPv6"))
        db_flux.append(Flux(hote_src=None, hote_dst=kwargs['instance'], type="ARP"))
        for peer_dst in Hote.objects.all():
            if peer_dst != kwargs['instance']:
                db_flux.append(Flux(hote_src=peer_dst, hote_dst=kwargs['instance'], type="IPv4"))
                db_flux.append(Flux(hote_src=kwargs['instance'], hote_dst=peer_dst, type="IPv4"))
                db_flux.append(Flux(hote_src=peer_dst, hote_dst=kwargs['instance'], type="IPv6"))
                db_flux.append(Flux(hote_src=kwargs['instance'], hote_dst=peer_dst, type="IPv6"))
        Flux.objects.bulk_create(db_flux)

@receiver(pre_delete, sender=Hote)
def pre_delete_hote(sender, **kwargs):
    # Retrieve all flux where the deleted host is present
    flux_list = Flux.objects.filter(Q(hote_src=kwargs['instance']) | Q(hote_dst=kwargs['instance']))
    # Remove stats from these flux
    Stats.objects.filter(idflux__in=flux_list).delete()
    # delete flux
    flux_list.delete()