import configparser
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

nomeBanco = cfg['DEFAULT']['NomeBanco']
codEntidade = cfg['DEFAULT']['CodEntidade']
nomeEntidade = cfg['DEFAULT']['NomeEntidade']
motorista = cfg['DEFAULT']['Motorista']

scripts = {

'Cor' : f""" SELECT distinct
upper(coalesce(cor,'Conversão')) ||'|'
FROM "Frotas".veiculos_equipamentos as exportCor """,

'Marca' : f""" SELECT
distinct m.descricao ||'|' as extractMarca
FROM "Frotas".veiculos_equipamentos v
join "Frotas".modelos_veiculos md on (md.id_registro = v.modelo_veiculo)
join "Frotas".marcas m on (m.codigo_marca = md.codigo_marca) """,

'Modelo' : f""" SELECT
mv.descricao ||'|'||
m.descricao ||'|'||
tve.descricao ||'|'||
'' ||'|' as extractespecie
FROM "Frotas".veiculos_equipamentos v
join "Frotas".modelos_veiculos mv on (mv.id_registro = v.modelo_veiculo)
join "Frotas".marcas m on (m.codigo_marca = mv.codigo_marca)
join "Frotas".tipo_veiculos_equipamentos tve on (tve.id_registro = v.tipo_veiculo_equipamento) """,

'Especie' : f""" SELECT distinct
tve.descricao ||'|'||
'B' ||'|' as ExtractCategoriaCNH
FROM "Frotas".veiculos_equipamentos v
join "Frotas".tipo_veiculos_equipamentos tve on (tve.id_registro = v.tipo_veiculo_equipamento) """,

'Motorista' : f""" SELECT
{codEntidade} ||'|'||
m.codigo_pessoa ||'|'||
'' ||'|'||
m.codigo_pessoa ||'|'||
lpad(cast(p.cpf_cnpj as varchar),11,'0') ||'|'||
lpad(cast(p.cpf_cnpj as varchar),11,'0') ||'|'||
'1' ||'|'|| -- (1-com foto, 2-sem foto)
substring(p.data_hora_criacao from 9 for 2) ||'/'|| substring(p.data_hora_criacao from 6 for 2) ||'/'|| substring(p.data_hora_criacao from 1 for 4) ||'|'||
DATE_PART('day',(SELECT CURRENT_DATE)) ||'/'|| DATE_PART('month',(SELECT CURRENT_DATE))+3 ||'/'|| DATE_PART('YEAR',(SELECT CURRENT_DATE)) ||'|'||
DATE_PART('day',(SELECT CURRENT_DATE)) ||'/'|| DATE_PART('month',(SELECT CURRENT_DATE)) ||'/'|| DATE_PART('YEAR',(SELECT CURRENT_DATE)) ||'|' as extractMotorista
FROM "Frotas".motoristas m
join "Frotas".pessoa p on (p.id_registro = m.codigo_pessoa) """,

'MotoristaCategoriaCnh' : f""" SELECT
{codEntidade} ||'|'||
m.codigo_pessoa ||'|'||
'B' ||'|' as MotoristaCategoriaCnh
FROM "Frotas".motoristas m """,

'MotoristaSituacaoCnh' : f""" SELECT
{codEntidade} ||'|'||
m.codigo_pessoa ||'|'||
DATE_PART('day',(SELECT CURRENT_DATE)) ||'/'|| DATE_PART('month',(SELECT CURRENT_DATE)) ||'/'|| DATE_PART('YEAR',(SELECT CURRENT_DATE)) ||'|'||
'1' ||'|'|| --(1- Normal, 2- Suspenso)
'0' ||'|' as extractMotoristaSituacaoCnh
FROM "Frotas".motoristas m """,

'Veiculo' : f""" SELECT
{codEntidade} ||'|'||
v.id_registro ||'|'||
--coalesce(cast(v.nro_patrimonio as varchar), '') ||'|'||
case v.id_registro
when 20334 then 860
when 20335 then 930
when 20336 then 1071
when 20337 then 1099 end ||'|'||
v.placa ||'|'||
tve.descricao ||'|'||
mv.descricao ||'|'||
coalesce(v.cor, 'CONVERSÃO') ||'|'||
v.renavam ||'|'||
v.chassi ||'|'||
'' ||'|'||
v.ano_fabricacao ||'|'||
v.ano_modelo ||'|'||
v.num_passageiros_veiculo ||'|'||
coalesce('Inativado: ' || v.data_inativacao, '') ||'|'||
'1' ||'|'|| -- (1- Sim 2- Não)
case v.vinculo
when 'P' then '1'
when 'T' then '2'
else '' end ||'|'|| -- (1- Próprio 2- Terceiro)
case em.nome
when 'GASOLINA COMUM' then '1'
when 'ETANOL' then '2'
else '' end ||'|'||
substring(v.data_aquisicao from 9 for 2) ||'/'|| substring(v.data_aquisicao from 6 for 2) ||'/'|| substring(v.data_aquisicao from 1 for 4) ||'|'||
'0' ||'|'||
'0' ||'|'||
v2.capacidade_volumetrica ||'|'||
'0' ||'|'||
'1' ||'|'||
'' ||'|' as extractVeiculo
FROM "Frotas".veiculos_equipamentos v
join "Frotas".modelos_veiculos mv on (mv.id_registro = v.modelo_veiculo)
join "Frotas".marcas m on (m.codigo_marca = mv.codigo_marca)
join "Frotas".tipo_veiculos_equipamentos tve on (tve.id_registro = v.tipo_veiculo_equipamento)
join "Frotas".veiculos_equipamentos_02 v2 on (v2.id_veiculo = v.id_registro)
join "Frotas".especificacoes_materiais em on (em.codigo_material = v2.codigo_material) """,

'Produto' : f""" SELECT
m.nome ||'|'||
m.codigo_material ||'|'||
'1' ||'|'|| -- (1- Combustivel, 2- Óleo Lubr, 3- Peças, 4- Serviços, 5- Pneus, 6- Acessórios)
'' ||'|'||
'' ||'|'||
'1' ||'|' as extractProduto
FROM "Frotas".especificacoes_materiais m
where m.id_registro in (4136729, 4776532) """,

'VeiculoProduto' : f""" select
{codEntidade} ||'|'||
v2.id_veiculo ||'|'||
v2.codigo_material ||'|'||
m.nome ||'|' as extractVeiculoProduto
from "Frotas".veiculos_equipamentos_02 v2
join "Frotas".especificacoes_materiais m on (m.codigo_material = v2.codigo_material) """,

'Abastecimento' : f""" select
{codEntidade} ||'|'||
l.num_lancto_despesa ||'|'||
l.id_veiculo ||'|'||
--coalesce(cast (v.nro_patrimonio as varchar),'') ||'|'||
case v.id_registro
when 20334 then 860
when 20335 then 930
when 20336 then 1071
when 20337 then 1099 end ||'|'||
v2.codigo_material ||'|'||
m.nome ||'|'||
l.codigo_motorista ||'|'||
replace(cast(l2.valor_unitario_item as varchar), '.',',') ||'|'||
substring(l.data_lancto_despesa from 9 for 2) ||'/'|| substring(l.data_lancto_despesa from 6 for 2) ||'/'|| substring(l.data_lancto_despesa from 1 for 4) ||' '|| substring(l.data_lancto_despesa from 12 for 8) ||'|'||
replace(cast(l2.qtde_item as varchar),'.',',') ||'|'||
replace(cast(l2.valor_total_item as varchar),'.',',') ||'|'||
case l2.completar_tanque
when 'S' then '1'
when 'N' then '2' end ||'|'||
l.num_doc ||'|'||
'' ||'|'||
l.codigo_fornecedor ||'|'||
lpad(cast(p.cpf_cnpj as varchar),14,'0') ||'|'||
'' ||'|'||
loc.codigo_config ||'|'||
'' ||'|'||
'1' ||'|'|| -- 1 = Sim - 2=Não
'' ||'|'||
'' ||'|'||
'' ||'|'||
'' ||'|'||
{codEntidade} ||'|'||
{codEntidade} ||'|'||
coalesce(cast(e.ano_empenho as varchar),'') ||'|'||
coalesce(cast(e.codigo_empenho as varchar),'') ||'|'||
coalesce(cast(e.ano_empenho as varchar),'') ||'|'||
{codEntidade} ||'|'||
coalesce(cast(l2.i_contabil_empenhos as varchar),'') ||'|' as extractAbastecimento
from "Frotas".lancto_despesas l
join "Frotas".veiculos_equipamentos v on (v.id_registro = l.id_veiculo)
join "Frotas".veiculos_equipamentos_02 v2 on (v2.id_veiculo = v.id_registro)
join "Frotas".especificacoes_materiais m on (m.codigo_material = v2.codigo_material)
join "Frotas".itens_lancto_despesas l2 on (l2.codigo_lancto_despesas = l.id_registro)
join "Frotas".pessoa p on (p.id_registro = l.codigo_fornecedor)
join "Frotas".organogramas loc on (loc.codigo_organogramas_contratos = l.codigo_organogramas_contratos)
left join "Frotas".empenhos_vindos_sistema_contabil e on (e.id_empenho = l2.i_contabil_empenhos) """,

'Acumulador' : f""" SELECT
{codEntidade} ||'|'||
a.id_veiculo ||'|'||
--coalesce(cast(v.nro_patrimonio as varchar),'') ||'|'||
case v.id_registro
when 20334 then 860
when 20335 then 930
when 20336 then 1071
when 20337 then 1099 end ||'|'||
substring(a.data_hora_criacao from 9 for 2) ||'/'|| substring(a.data_hora_criacao from 6 for 2) ||'/'|| substring(a.data_hora_criacao from 1 for 4) ||' '|| substring(a.data_hora_criacao from 12 for 4) ||'#min#:#sec#|'||
2 ||'|'|| -- 2 - Abastecimento
a.num_lancto_despesa ||'|'||
a.qtde_unidade_operacional ||'|'||
a.qtde_unidade_operacional ||'|' as extractAcumulador
FROM "Frotas".lancto_despesas a
join "Frotas".veiculos_equipamentos v on (v.id_registro = a.id_veiculo)
order by a.num_lancto_despesa """,

'VeiculoControleSimAm' : f""" SELECT 
{codEntidade} ||'|'||
ctr.codigo_entidade_01 ||'|'||
'#seq#' ||'|'||
'1' ||'|'||
substring(ctr.competencia from 9 for 2) ||'/'|| substring(ctr.competencia from 6 for 2) ||'/'|| substring(ctr.competencia from 1 for 4) ||'|'||
'0' ||'|'||
'' ||'|'||
ctr.marcador ||'|'||
case ctr.quebrou_marcador 
    when 'N' then 2
    when 'S' then 1 end ||'|'||
ctr.marcacao_inicial ||'|'||
ctr.marcacao_final ||'|'||
'0,00' ||'|'||
'' ||'|' as extractVeiculoControleSimAm
FROM "Frotas".acompanhamento_mensal_veiculos ctr
order by ctr.codigo_entidade_01, substring(ctr.competencia from 1 for 4), substring(ctr.competencia from 6 for 2) """

}